#!/bin/bash
set -e

# Parse args
model_in="$1"
model_in_name="$(basename ${model_in%.*})"
model_out="$2"

# Setup SGX if necessary
if [[ ! -f train.token && "$LOADER" == "gramine-sgx" ]]; then
    ./sgx-setup.sh train
fi

# Convert npz to pt
python helper.py np2pt "$model_in" "$TMPDIR/$model_in_name".pt

# Train
export N_SPLITS=$(sudo docker ps --format "{{ .Names }}" | grep client | wc -l)
SPLIT=$(sudo docker ps | grep $(hostname) | awk '{print substr($NF, length($NF), length($NF))}')
export SPLIT=$(($SPLIT - 1))
export OMP_NUM_THREADS=4
$LOADER ./train "$TMPDIR/$model_in_name".pt "$TMPDIR/$model_in_name".retrain.pt

# Convert pt to npz
python helper.py pt2np "$TMPDIR/$model_in_name".retrain.pt "$model_out"