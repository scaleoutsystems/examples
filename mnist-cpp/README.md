# MNIST example - Pytorch C++
This is an example of the classic MNIST hand-written text recognition task using FEDn with the PyTorch C++ API.

## Table of Contents
- [MNIST example - Pytorch C++](#mnist-example---pytorch-c)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Running the example](#running-the-example)
  - [Clean up](#clean-up)

## Prerequisites
The only prerequisite to run this example is [Docker](https://www.docker.com).

## Running the example

Start by downloading the data:

```
bin/download_data.sh
```

Start the Docker environment:
```
bin/launch.sh
```
> This may take a few minutes.

Build the compute package and train the seed model:
```
bin/build.sh
```
> This may take a few minutes. After completion `package/package.tgz` and `seed.npz` should be built in your current working directory.

Start reduce and combiner network:
```
sudo docker-compose up -d
```
> This may take a few minutes. After this is done you should be able to access the reducer interface at https://localhost:8090.

Now navigate to https://localhost:8090 and upload `package/package.tgz` and `seed.npz`. After you are done you can deploy two clients by running:
```
sudo docker-compose up -d --scale client=2
```

Finally, you can navigate again to https://localhost:8090 and start the experiment from the "control" tab.

## Clean up
To clean up you can run: `docker-compose down`. To exit the Docker environment simply run `exit`.