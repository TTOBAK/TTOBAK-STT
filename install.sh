#!/bin/bash

. ./config.sh

cp config.sh $ZEROTH_ROOT/config.sh

cp run_custom.sh $ZEROTH_ROOT/run_custom.sh

cp calc_pron_score.py $ZEROTH_ROOT/local/calc_pron_score.py
cp result2phone.py $ZEROTH_ROOT/local/result2phone.py
cp result2time.py $ZEROTH_ROOT/local/result2time.py
cp result2word.py $ZEROTH_ROOT/local/result2word.py
cp data_prep_single.sh $ZEROTH_ROOT/local/data_prep_single.sh
cp scripts/genPhoneSeq.py $ZEROTH_ROOT/local/genPhoneSeq.py

ln -sfn $ZEROTH_ROOT/path.sh path.sh
