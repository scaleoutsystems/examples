#!/bin/bash

# Parse args
src=$1

# Generate SGX files
openssl genrsa -3 -out enclave-key.pem 3072
gramine-manifest -Dlog_level=debug $src.manifest.template $src.manifest
gramine-sgx-sign --key enclave-key.pem --manifest $src.manifest --output $src.manifest.sgx
gramine-sgx-get-token --output $src.token --sig $src.sig