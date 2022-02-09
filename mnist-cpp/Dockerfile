# Base image
FROM debian:bookworm

# Env versioning
ARG HADOLINT_VERSION=v2.8.0
ARG CMAKE_VERSION=3.16.9
ARG TORCH_VERSION=1.10.1
ARG NUMCPP_VERSION=2.6.2
ARG DOCKER_VERSION=19.03.9
ARG CONDA_VERSION=4.9.2
ARG COMPOSE_VERSION=1.29.2
ARG SGX_SDK_VERSION=2.15.101.1
ARG SGX_PSW_VERSION=2.15.1
ARG GRAMINE_HEAD=v1.1

# Non-root user with sudo access
ARG USERNAME=default
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Other env
ENV TORCH_DIR=/opt/torch
ENV DATA_DIR=/app/data

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
  openssh-client \
  build-essential \
  autoconf \
  libtool \
  pkg-config \
  googletest \
  libgtest-dev \
  autoconf \
  gawk \
  libcurl4-openssl-dev \
  libprotobuf-c-dev \
  protobuf-c-compiler \
  linux-headers-amd64 \
  unzip \
  bison \
  #
  # Hadolint
  && wget --progress=dot:giga -O /bin/hadolint \
  https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-x86_64 \
  && chmod +x /bin/hadolint \
  #
  # Install docker binaries
  && curl -L https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz | tar xvz docker/docker \
  && cp docker/docker /usr/local/bin \
  && rm -R docker \
  && curl -L https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose \
  && chmod +x /usr/local/bin/docker-compose \
  #
  # Install cmake
  && wget -q -O cmake-linux.sh https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.sh \
  && sh cmake-linux.sh -- --skip-license \
  && rm cmake-linux.sh \
  # 
  # Install libtorch
  && mkdir $TORCH_DIR \
  && pushd $TORCH_DIR \
  && wget --progress=dot:giga https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-${TORCH_VERSION}%2Bcpu.zip \
  && unzip libtorch-cxx11-abi-shared-with-deps-${TORCH_VERSION}+cpu.zip \
  && rm -r libtorch-cxx11-abi-shared-with-deps-${TORCH_VERSION}+cpu.zip \
  && popd \
  #
  # SGX SDK
  && wget --progress=dot:giga https://download.01.org/intel-sgx/latest/linux-latest/distro/ubuntu20.04-server/sgx_linux_x64_sdk_${SGX_SDK_VERSION}.bin \
  && chmod +x sgx_linux_x64_sdk_${SGX_SDK_VERSION}.bin \
  && ./sgx_linux_x64_sdk_${SGX_SDK_VERSION}.bin --prefix /opt/sgx-sdk \
  && rm sgx_linux_x64_sdk_${SGX_SDK_VERSION}.bin \
  #
  # SGX PSW
  && wget --progress=dot:giga https://download.01.org/intel-sgx/sgx-linux/${SGX_PSW_VERSION}/distro/ubuntu20.04-server/sgx_debian_local_repo.tgz \
  && tar xzvf sgx_debian_local_repo.tgz \
  && mv sgx_debian_local_repo /opt \
  && echo 'deb [trusted=yes] file:///opt/sgx_debian_local_repo focal main' >> /etc/apt/sources.list \
  && echo 'deb [trusted=yes] http://archive.ubuntu.com/ubuntu focal main' >> /etc/apt/sources.list \
  && apt-get update \
  && sudo apt-get install -y --no-install-recommends \
  ubuntu-keyring \
  libsgx-urts \
  libsgx-launch \
  libsgx-epid \
  libsgx-quote-ex \
  libsgx-dcap-ql \
  # 
  # Install conda
  && wget --progress=dot:giga https://repo.anaconda.com/miniconda/Miniconda3-py39_${CONDA_VERSION}-Linux-x86_64.sh \
  && bash Miniconda3-py39_${CONDA_VERSION}-Linux-x86_64.sh -b -p /opt/conda \
  && rm -f Miniconda3-py39_${CONDA_VERSION}-Linux-x86_64.sh \
  && ln -s /opt/conda/bin/conda /bin/conda \
  && ln -s /opt/conda/bin/conda-env /bin/conda-env \
  #
  # Create a non-root user to use if preferred
  && groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  #
  # Configure FEDn directories
  && mkdir -p /app/certs \
  && mkdir -p /app/client/package \
  && mkdir -p /app/config \
  && chown -R $USERNAME /app \
  #
  # Configure data dir
  && mkdir -p $DATA_DIR \
  && chown $USERNAME $DATA_DIR \
  #
  # Configure for gramine
  && mkdir -p /usr/include/asm \
  && ln -s /usr/src/linux-headers-*/arch/x86/include/uapi/asm/sgx.h /usr/include/asm/sgx.h \
  && mkdir -p /opt/gramine \
  && chown -R $USERNAME /opt/gramine \
  #
  # Cleanup
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Copy FEDn config
COPY config/*.yaml /app/config/

# Setup default environment
COPY environment.yaml /tmp/environment.yaml
RUN conda env create -f /tmp/environment.yaml \
  && rm /tmp/environment.yaml \
  && conda run -n default python -m ipykernel install --name default \
  && chown $USERNAME /opt/conda/envs/default

# Init conda for non-root user
USER $USERNAME
RUN conda init bash \
  && conda config --set auto_activate_base false \
  && echo "conda activate default" >> ~/.bashrc

# Gramine
RUN git clone https://github.com/gramineproject/gramine.git /opt/gramine \
  && pushd /opt/gramine \
  && git checkout $GRAMINE_HEAD \
  && conda run -n default meson setup build/ \
  --buildtype=release -Ddirect=enabled -Dsgx=enabled --prefix=/opt/conda/envs/default \
  && conda run -n default ninja -C build/ \
  && sudo /opt/conda/envs/default/bin/ninja -C build/ install \
  && popd

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# Add entrypoint to conda environment for commands
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "default"]