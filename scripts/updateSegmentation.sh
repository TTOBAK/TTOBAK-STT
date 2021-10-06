#!/bin/bash

# Copyright 2017 Lucas Jo (Atlas Guide)
# Apache 2.0

# do this when the segmentation rule is changed
# $KALDI_ROOT/tools/extras/install_morfessor.sh is merged 
# at revision 5e6bd39e0ec0e510cb7202990c22fe8b8b9d817c
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <data-dir> <lm-dir>"
    echo "   ex: $0 data/train_data_01 data/local/lm"
    exit 1
fi
dataDir=$1
lmDir=$2

. ../path.sh
trans=$dataDir/text
echo "Re-segment transcripts: $trans --------------------------------------------"
if [ ! -f $trans ]; then
	echo "transcription file is not found in "$dataDir
	exit 1
fi

base=$(basename $dataDir)
cp $trans $trans".copy"
cp $trans $trans".old"
awk '{print $1}' $trans".old" > $trans"_tmp_index"
cut -d' ' -f2- $trans".old" |\
	sed -E 's/\s+/ /g; s/^\s//g; s/\s$//g' |\
	morfessor -l $lmDir/zeroth_morfessor.seg -T - -o - \
	--output-format '{analysis} ' --output-newlines \
	--nosplit-re '[0-9\[\]\(\){}a-zA-Z&.,\-]+' \
	| paste -d" " $trans"_tmp_index" - > $trans".copy"
\cp $trans".copy" $dataDir/$base".trans.txt"
rm -f $trans"_tmp_index" $trans".old" $trans".copy"
