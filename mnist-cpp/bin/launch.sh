#!/bin/bash
set -e

# Build container
docker build \
	-f Dockerfile \
	-t local/mnist-cpp \
	--build-arg DOCKER_USER=$(whoami) \
	--build-arg USER_UID=$UID \
	--build-arg $(id -u $USER) \
	.

# Run
docker run --rm -it \
	-v $PWD:/mnist-cpp -w /mnist-cpp \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v $PWD/data:/app/data \
	--net=host \
	-u default \
	local/mnist-cpp \
	/bin/bash -c "echo HOST_DATA_DIR=$PWD/data > .env && /bin/bash"