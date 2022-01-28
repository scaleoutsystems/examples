{
  "name": "devcontainer",
  "dockerFile": "../Dockerfile",
  "context": "..",
  "remoteUser": "default",
  "extensions": [
    "ms-vscode.cpptools",
    "ms-vscode.cpptools-extension-pack",
    "ms-vscode.cpptools-themes",
    "exiasr.hadolint",
    "yzhang.markdown-all-in-one",
    "ms-python.python",
    "ms-toolsai.jupyter",
    "ms-azuretools.vscode-docker"
  ],
  "mounts": [
    "source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind,consistency=default",
  ],
  "runArgs": [
    "--net=host"
  ],
  "forwardPorts": [8090, 9000, 9001, 8081],
}