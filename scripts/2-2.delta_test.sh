#!/bin/bash

dataset="mimic_cxr"
annotation="./data/"
base_dir="./data/ALMM/physionet.org/files/mimic-cxr-jpg/2.0.0/files/"
delta_file=""

version="v1_delta"
savepath="./save/$dataset/$version"

CUDA_VISIBLE_DEVICES=0 python -u train.py \
    --test \
    --dataset ${dataset} \
    --annotation ${annotation} \
    --base_dir ${base_dir} \
    --delta_file ${delta_file} \
    --max_length 100 \
    --min_new_tokens 80 \
    --max_new_tokens 120 \
    --repetition_penalty 2.0 \
    --length_penalty 2.0 \
    --test_batch_size 16 \
    --freeze_vm True \
    --vis_use_lora True \
    --vis_r 16 \
    --vis_alpha 16 \
    --savedmodel_path ${savepath} \
    --num_workers 12 \
    --devices 1 \
    2>&1 |tee -a ${savepath}/log.txt
