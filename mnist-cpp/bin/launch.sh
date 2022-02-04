#!/bin/bash
set -e

# Build container
docker build \
	-f Dockerfile \
	-t local/mnist-cpp \
	--build-arg DOCKER_USER=$(whoami) \
	--build-arg USER_UID=$UID \
	.

# Run
if [ -z "$HOST_DATA_DIR" ]; then HOST_DATA_DIR="$PWD/data"; fi
if [ -z "$HOST_WRKSPC_DIR" ]; then HOST_WRKSPC_DIR="$PWD"; fi
docker run --rm -it \
	-v "$HOST_WRKSPC_DIR:/mnist-cpp" -w /mnist-cpp \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v "$HOST_DATA_DIR:/app/data" \
	--net=host \
	-u default \
	local/mnist-cpp \
	/bin/bash -c "set -C; echo HOST_DATA_DIR=$HOST_DATA_DIR > .env; /bin/bash"