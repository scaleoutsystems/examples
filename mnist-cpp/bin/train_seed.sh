#!/bin/bash
set -e

# Train
N_SPLITS=1 SPLIT=0 client/train seed.pt

# Make npz
python client/helper.py pt2np seed.pt seed