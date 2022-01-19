# Base image
FROM debian:bookworm

# Env versioning
ARG HADOLINT_VERSION=v2.8.0
ARG CMAKE_VERSION=3.16.9
ARG TORCH_VERSION=1.10.1
ARG NUMCPP_VERSION=2.6.2
ARG DOCKER_VERSION=19.03.9
ARG CONDA_VERSION=4.9.2

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
  && curl -L https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz | tar xvz docker/docker \
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
  # Install conda
  && wget https://repo.anaconda.com/miniconda/Miniconda3-py39_${CONDA_VERSION}-Linux-x86_64.sh \
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
  # Cleanup
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Setup default environment
COPY environment.yaml /tmp/environment.yaml
RUN conda env create -f /tmp/environment.yaml \
  && rm /tmp/environment.yaml \
  && conda run -n default python -m ipykernel install --name default \
  && chown default /opt/conda/envs/default

# Init conda for non-root user
USER $USERNAME
RUN conda init bash \
  && conda config --set auto_activate_base false \
  && echo "conda activate default" >> ~/.bashrc

# Set working directory
WORKDIR /home/$USERNAME

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog