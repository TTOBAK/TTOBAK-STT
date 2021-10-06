#!/usr/bin/env bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <gender> <transcript> <file>"
  echo "e.g.: $0 m '안녕하세요 반갑습니다' test4.m4a"
  exit 1
fi

. ./config.sh
. ./path.sh

gender=$1
transcript=$2
file=$3

file_path=$PWD/server/temp/raw/$file
result_file_path=$PWD/server/temp/result/$file.json

id=$(($(date +%s%N)/1000000))

course=$id
if [ $gender = 'm' ]; then
    user=100
else
    user=101
fi

data=$BASE_DIR/data
log=$BASE_DIR/log
trans=$log/trans/$id
ali=$log/ali/$id
make_mfcc=$log/make_mfcc
mfcc=$log/mfcc

model=$BASE_DIR/model

final=$FINAL_DIR/result

exp=$model/chain_rvb

decoder=$KALDI_ROOT/src/online2bin/online2-wav-nnet3-latgen-faster

cmd="run.pl --mem 2G"

startTime=startTime=$(date +'%F %H:%M:%S')
echo $startTime

if [ ! -d $log ]; then
    mkdir $log;
    mkdir $log/trans;
    mkdir $log/ali;
    mkdir $log/make_mfcc;
    mkdir $log/mfcc;
fi

if [ ! -d $final ]; then
    mkdir $final;
fi

cd $ZEROTH_ROOT

mkdir $data/$course

mkdir $data/$course/$user

echo $transcript > $data/$course/text
echo $transcript > $data/$course/$course.trans.txt

ffmpeg -y -i $file_path -sample_fmt s16 -ar 16000 $data/$course/$user/${course}_${user}_${id}.flac
cp $data/$course/$user/${course}_${user}_${id}.flac $final/${course}_${user}_${id}.flac

# data 준비(AUDIO_INFO 파일과 trans.txt 파일 필수)
mkdir $trans
local/data_prep_single.sh $data/$course/$user/${course}_${user}_${id}.flac $course $user $data $trans

# phone generation
python3 local/genPhoneSeq.py $data/$course/$course.trans.txt $data/$course/$course.prons.txt

# decode
mkdir $ali
$decoder --do-endpointing=false \
	--frames-per-chunk=20 \
	--extra-left-context-initial=0 \
	--online=false \
	--config=$exp/tdnn1n_rvb_online/conf/online.conf \
	--verbose=2 \
	--min-active=200 --max-active=7000 --beam=1.0 --lattice-beam=6.0 \
	--acoustic-scale=3.0 \
	--frame-subsampling-factor=3 \
	--word-symbol-table=$exp/tree_a/graph_tgsmall/words.txt \
	$exp/tdnn1n_rvb_online/final.mdl $exp/tree_a/graph_tgsmall/HCLG.fst "ark:$trans/spk2utt" "scp,p:$trans/wav.scp" \
	"ark:|gzip -c >$ali/lat.1.gz"

# 단어 형태의 lattice를 음소 형태로 변환
$KALDI_ROOT/src/latbin/lattice-align-phones --replace-output-symbols=true $exp/tdnn1n_rvb_online/final.mdl "ark:gunzip -c ${ali}/lat.1.gz|" ark:$ali/phone_aligned.lats

# 가장 확률이 높은 1가지 경우를 선택
$KALDI_ROOT/src/latbin/lattice-best-path ark:$ali/phone_aligned.lats ark:$ali/out.tra ark:$ali/out.ali

# align을 발음 sequence를 포함한 파일로 출력
$KALDI_ROOT/src/bin/show-alignments $exp/tree_a/graph_tgsmall/phones.txt $exp/tdnn1n_rvb_online/final.mdl ark:$ali/out.ali >> $ali/temp.txt

# 파일을 단어 sequence로 변환
python3 $ZEROTH_ROOT/local/result2word.py $ali/temp.txt $ali/word.txt

# 파일을 phone sequence로 변환
python3 $ZEROTH_ROOT/local/result2time.py $ali/temp.txt $ali/result.json

# 발음 정확도 계산
python3 $ZEROTH_ROOT/local/calc_pron_score.py $ali/result.json $ali/word.txt $data/$course/${course}.prons.txt $data/$course/text $final/${course}_${user}_${id}.json

cp $final/${course}_${user}_${id}.json $result_file_path

rm -rf $data/$course

endTime=$(date +'%F %H:%M:%S')
echo $endTime


