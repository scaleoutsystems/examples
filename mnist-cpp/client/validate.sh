#!/bin/bash
set -e

# Parse args
model_in="$1"
model_in_name="$(basename ${model_in%.*})"
json_out="$2"

# Setup SGX if necessary
if [[ ! -f validate.token && "$LOADER" == "gramine-sgx" ]]; then
    ./sgx-setup.sh validate
fi

# Convert npz to pt
python helper.py np2pt "$model_in" "$TMPDIR/$model_in_name".pt

# Validate
export OMP_NUM_THREADS=2
$LOADER ./validate "$TMPDIR/$model_in_name".pt "$json_out"