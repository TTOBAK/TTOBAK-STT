#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 <file> <src-dir> <dst-dir>"
  echo "e.g.: $0 1.flac /export/a15/vpanayotov/data/LibriSpeech/dev-clean data/dev-clean"
  exit 1
fi

file=$1
#file=~/PycharmProjects/data/00008024/104/00008024_104_1595070537522.flac
scriptid=$2
reader=$3
src=$4
dst=$5

filename=$(basename $file .flac)
scriptid_dir=$src/$scriptid

# all utterances are FLAC compressed
if ! which flac >&/dev/null; then
   echo "Please install 'flac' on ALL worker nodes!"
   exit 1
fi

spk_file=$src/AUDIO_INFO

mkdir -p $dst || exit 1;

[ ! -d $src ] && echo "$0: no such directory $src" && exit 1;
[ ! -f $spk_file ] && echo "$0: expected file $spk_file to exist" && exit 1;

wav_scp=$dst/wav.scp; [[ -f "$wav_scp" ]] && rm $wav_scp
trans=$dst/text; [[ -f "$trans" ]] && rm $trans
utt2spk=$dst/utt2spk; [[ -f "$utt2spk" ]] && rm $utt2spk
spk2gender=$dst/spk2gender; [[ -f $spk2gender ]] && rm $spk2gender
utt2dur=$dst/utt2dur; [[ -f "$utt2dur" ]] && rm $utt2dur

reader_gender=$(egrep "^$reader\|" $spk_file |  awk -F'|' '{gsub(/[ ]+/, ""); print tolower($3)}')
if [ "$reader_gender" != 'm' ] && [ "$reader_gender" != 'f' ]; then
  echo "Unexpected gender: '$reader_gender'"
  exit 1;
fi

echo "  "$scriptid $reader $reader_gender

echo "${filename} flac -c -d -s ${file} |" >>$wav_scp

reader_trans=$scriptid_dir/${scriptid}.trans.txt
[ ! -f  $reader_trans ] && echo "$0: expected file $reader_trans to exist" && exit 1
awk -v "fname=$filename" '{printf "%s %s", fname, $0}' <$reader_trans >>$trans || exit 1

# NOTE: For now we are using per-chapter utt2spk. That is each chapter is considered
#       to be a different speaker. This is done for simplicity and because we want
#       e.g. the CMVN to be calculated per-chapter
awk -v "fname=$filename" -v "reader=$reader" -v "scriptid=$scriptid" '{printf "%s %s_%s\n", fname, scriptid, reader}' \
  <$reader_trans >>$utt2spk || exit 1

# reader -> gender map (again using per-chapter granularity)
echo "${scriptid}_${reader} $reader_gender" >>$spk2gender

# sort
cat $wav_scp    | sort > tmp
cp tmp $wav_scp
cat $trans      | sort > tmp
cp tmp $trans
cat $utt2spk    | sort > tmp
cp tmp $utt2spk
cat $spk2gender | sort > tmp
cp tmp $spk2gender
rm tmp


spk2utt=$dst/spk2utt
utils/utt2spk_to_spk2utt.pl <$utt2spk >$spk2utt || exit 1

ntrans=$(wc -l <$trans)
nutt2spk=$(wc -l <$utt2spk)
! [ "$ntrans" -eq "$nutt2spk" ] && \
  echo "Inconsistent #transcripts($ntrans) and #utt2spk($nutt2spk)" && exit 1;

utils/data/get_utt2dur.sh $dst 1>&2 || exit 1

utils/validate_data_dir.sh --no-feats $dst || exit 1;

echo "$0: successfully prepared data in $dst"

exit 0