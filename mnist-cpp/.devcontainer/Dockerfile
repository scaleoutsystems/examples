# Base image
FROM debian:bookworm

# Env versioning
ARG HADOLINT_VERSION=v2.8.0
ARG CMAKE_VERSION=3.16.9
ARG TORCH_VERSION=1.10.1

# Non-root user with sudo access
ARG USERNAME=default
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Other env
ENV TORCH_DIR=/opt/torch

# Install apt deps
SHELL ["/bin/bash", "-c"]
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  apt-utils \
  dialog 2>&1 \
  #
  # More apt deps
  && apt-get install -y --no-install-recommends \
  sudo \
  ca-certificates \
  wget \
  curl \
  git \
  vim \
  build-essential \
  unzip \
  openssh-client \
  #
  # Hadolint
  && wget --progress=dot:giga -O /bin/hadolint \
  https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-x86_64 \
  && chmod +x /bin/hadolint \
  #
  # Install docker binary
  && curl -L https://download.docker.com/linux/static/stable/x86_64/docker-19.03.9.tgz | tar xvz docker/docker \
  && cp docker/docker /usr/local/bin \
  && rm -R docker \
  #
  # Install cmake
  && wget -q -O cmake-linux.sh https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.sh \
  && sh cmake-linux.sh -- --skip-license \
  && rm cmake-linux.sh \
  # 
  # Install libtorch
  && mkdir $TORCH_DIR \
  && pushd $TORCH_DIR \
  && wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-${TORCH_VERSION}%2Bcpu.zip \
  && unzip libtorch-cxx11-abi-shared-with-deps-${TORCH_VERSION}+cpu.zip \
  && rm -r libtorch-cxx11-abi-shared-with-deps-${TORCH_VERSION}+cpu.zip \
  && popd \
  #
  # Create a non-root user to use if preferred
  && groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  #
  # Cleanup
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/$USERNAME

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog