#!/bin/bash
set -e

# Parse args
model_in="$1"
model_in_name="$(basename ${model_in%.*})"
model_out="$2"

# Convert npz to pt
python helper.py np2pt "$model_in" "$model_in_name".pt

# Train
export N_SPLITS=$(sudo docker ps --format "{{ .Names }}" | grep client | wc -l)
SPLIT=$(sudo docker ps | grep $(hostname) | awk '{print substr($NF, length($NF), length($NF))}')
export SPLIT=$(($SPLIT - 1))
export OMP_NUM_THREADS=2
$LOADER ./train "$model_in_name".pt "$model_in_name".retrain.pt

# Convert pt to npz
python helper.py pt2np "$model_in_name".retrain.pt "$model_out"