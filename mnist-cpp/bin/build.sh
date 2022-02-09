#!/bin/bash
set -e

# Configure
cmake --no-warn-unused-cli \
    -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE \
    -DCMAKE_BUILD_TYPE:STRING=Debug \
    -DCMAKE_C_COMPILER:FILEPATH=/usr/bin/x86_64-linux-gnu-gcc-11 \
    -DCMAKE_CXX_COMPILER:FILEPATH=/usr/bin/x86_64-linux-gnu-g++-11 \
    -H$PWD \
    -B$PWD/build \
    -G Ninja

# Build
cmake --build $PWD/build --config Debug --target all -j $(nproc) --

# Copy binaries to the right folder
cp build/train build/validate client

# Generate sig key if necessary
if [ ! -e "$HOME/.gramine/enclave-key.pem" ]; then
    mkdir -p $HOME/.gramine
    openssl genrsa -3 -out $HOME/.gramine/enclave-key.pem 3072
fi

# Generate SGX-related files
pushd client
for src in train validate; do
    gramine-manifest -Dlog_level=debug $src.manifest.template $src.manifest
    gramine-sgx-sign --key $HOME/.gramine/enclave-key.pem --manifest $src.manifest --output $src.manifest.sgx
    gramine-sgx-get-token --output $src.token --sig $src.sig
done
popd

# Make package
mkdir -p package
tar -czvf package/package.tar.gz client

# Make seed
SPLIT=0 N_SPLITS=1 build/train seed.pt
python client/helper.py pt2np seed.pt seed