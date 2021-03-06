#!/bin/bash

. ./path.sh
set -e

### Select GPU
if [ $# -ne 2 ]; then
  echo "Error: set GPU number & config path." 1>&2
  echo "Usage: ./decode_lm.sh path_to_saved_model gpu_id" 1>&2
  exit 1
fi

CUDA_VISIBLE_DEVICES=$2 ${PYTHON} ../../../src/bin/visualization/decode_lm.py \
  --corpus ${corpus} \
  --data_type test_clean \
  --data_save_path ${data} \
  --model_path $1 \
  --epoch -1 \
  --eval_batch_size 1
