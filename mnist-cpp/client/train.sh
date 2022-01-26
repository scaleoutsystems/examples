#!/bin/bash
set -e

# Parse args
model_in="$1"
model_in_name="$(basename ${model_in%.*})"
model_out="$2"

# Convert npz to pt
python helper.py np2pt "$model_in" "$model_in_name".pt

# Train
./train "$model_in_name".pt "$model_in_name".retrain.pt

# Convert pt to npz
python helper.py pt2np "$model_in_name".retrain.pt "$model_out"