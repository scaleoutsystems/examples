#!/bin/bash
set -e

# Parse args
model_in="$1"
model_in_name="$(basename ${model_in%.*})"
json_out="$2"

# Convert npz to pt
python helper.py np2pt "$model_in" "$model_in_name".pt

# Train
./validate "$model_in_name".pt "$json_out"