# CASA example - Keras version
This classsic example of Human Daily Activity Recognition (HDAR) is well suited both as a lightweight test when learning FEDn and developing on FEDn in psedo-distributed mode. A normal high-end laptop or a workstation should be able to sustain at least 15 clients. The example is also useful for general scalability tests in fully distributed mode, for more details about the dataset please check to the following link.

https://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+from+Continuous+Ambient+Sensor+Data


## Provide local training and test data
For large data transfer reason we uploaded a data folder in this use case to archive.org. To test this use case, you need to download prepared data that composed 27 apartments (casa's). In this use-case, two different ways have been provided to generate the dataset partitions (training, and testing set), that gives the user more flexibility, these ways are listed below.

1. Based on your needs (number of clients you want, the training dataset size, and testing dataset size), due to the large size of the dataset we provide a lightweight sample (http://archive.org/download/train_20211025/train.csv') of the dataset to prepare your partitions by downloading and preparing the dataset partitions (creates 10 partitions) in ./data/casa{index}/c{index}, using the following command.
```
python create_data_partitions.py
```
For the full dataset partitioning you need to download the dataset manually using the following command:
```
wget http://archive.org/download/all_20210914/all.csv
```
After having the full dataset locally, you have to replace the dataset path in ``` create_data_partitions.py ``` line 10 with the local dataset path, then execute the following command.
```
python create_data_partitions.py
```

2. Partitions already generated for each apartment the dataset is distributed over 11 clients (training and testing sets),  you can download it using the following command:
```
wget https://archive.org/download/data_20210225/data.zip
```
After that, please follow the next instructions.
   - Unzip the file
   - Copy the content of the unzipped Archive to the data folder under casa directory

## Configuring the Reducer
Navigate to 'https://localhost:8090' (or the url of your Reducer) and follow instructions to upload the compute package in 'package/package.tar.gz' and the initial model in 'initial_model/initial_model.npz'.

## Attaching a client to the federation
1. First, download 'client.yaml' from the Reducer 'Network' page, and replace the content in your local 'client.yaml'. 
2. Start a client. Here there are different options (see below): 
    - Docker 
    - docker-compose
    - [Native client (OSX/Linux)](https://github.com/scaleoutsystems/examples/tree/main/how-tos/start-native-fedn-client)
    
### Docker
1. Build the image

``` bash
docker build . -t casa:latest
```

2. Start a client (edit the path of the volume mounts to provide the absolute path to your local folder) and change the data partition in clients folder.
```
docker run -v /absolute-path-to-this-folder/data/clients/0:/app/data -v /absolute-path-to-this-folder/client.yaml:/app/client.yaml --network fedn_default casa fedn run client -in client.yaml 
```
(Repeat above steps as needed to deploy additional clients).

### docker-compose
To start 30 clients: 

```bash
docker-compose -f docker-compose.yaml -f private-network.yaml up 
```
> If you are connecting to a Reducer part of a distributed setup or in Studio, you should omit 'private-network.yaml'. 

### Native client on OSX/Linux
The compute package assumes that the local dataset in in a folder 'data' in the same folder as you start the client. Make a new folder and copy the data partition you want to use into data:
```bash
cp data/casa1/c1/*.csv data/
```
Then [follow the instructions here](https://github.com/scaleoutsystems/examples/tree/main/how-tos/start-native-fedn-client) to start the client. 

## Start training 
When clients are running, navigate to the 'Control' page of the Reducer to start the training. 



## Configuring the client
We have made it possible to configure a couple of settings to vary the conditions for the training. These configurations are expsosed in the file 'client/settings.yaml': 

```yaml 
# Parameters for local training
test_size: 0.25
batch_size: 32
epochs: 3
```

## Creating a compute package
Whenever you make updates to the client code (such as altering any of the settings in the above mentioned file), you need to re-package the compute package:

```bash
tar -czvf package.tar.gz client
```
To clear the system and set a new compute package, see: https://github.com/scaleoutsystems/fedn/blob/master/docs/FAQ.md

For an explaination of the compute package structure and content: https://github.com/scaleoutsystems/fedn/blob/develop/docs/tutorial.md
 
## Creating a new initial model
The baseline LSTM is specified in the file 'client/init_model.py'. This script creates an untrained neural network and serializes that to a file.  If you wish to alter the initial model, edit 'init_model.py' and 'models/casa_model.py' then regenerate the initial model file (install dependencies as needed, see requirements.txt):

```bash
python init_model.py 
```

## Generate the configuration files
We provide the 'generate_clients.sh' bash file to generate all the configuration yaml files (docker_compose.yaml, private-network.yaml, extra-hosts.yaml) to run casa benchmark in the easiest way.
```bash
bash generate_clients.sh 
```
## License
Apache-2.0 (see LICENSE file for full information).




[comment]: <> (## Start the client)

[comment]: <> (The easiest way to start clients for quick testing is by using Docker. We provide a docker-compose template for convenience. First, edit 'fedn-network.yaml' to provide information about the reducer endpoint. Then:)

[comment]: <> (```bash)

[comment]: <> (docker-compose -f docker-compose.yaml up --scale client=2 )

[comment]: <> (```)

[comment]: <> (> Note that this assumes that a FEDn network is running &#40;see separate deployment instructions&#41;. The file 'docker-compose.yaml' is for testing against a local pseudo-distributed FEDn network. Use 'docker-compose.decentralised.yaml' if you are connecting against a reducer part of a distributed setup and provide a 'extra_hosts' file.)

[comment]: <> (The easiest way to start clients for quick testing is by using Docker. We provide a docker-compose template for convenience. First, edit 'fedn-network.yaml' to provide information about the reducer endpoint. Then:)

[comment]: <> (The easiest way to distribute data across client is to start this command instead of the previous one )

[comment]: <> (```bash)

[comment]: <> (docker-compose -f docker-compose.decentralised.yaml up --build)

[comment]: <> (```)


[comment]: <> (## Configure and start a client using cpu device)

[comment]: <> (The easiest way to start clients for quick testing is to use shell script.The following )

[comment]: <> (shell script will configure and start a client on a blank Ubuntu 20.04 LTS VM:    )


[comment]: <> (```bash)

[comment]: <> (#!/bin/bash)

[comment]: <> (# Install Docker and docker-compose)

[comment]: <> (sudo apt-get update)

[comment]: <> (sudo sudo snap install docker)

[comment]: <> (# clone the nlp_imdb example)

[comment]: <> (git https://github.com/scaleoutsystems/FEDn-client-casa-keras.git)

[comment]: <> (cd FEDn-client-casa-keras)

[comment]: <> (# if no available data, download it from archive)

[comment]: <> (# wget https://archive.org/download/data_20210225/data.zip)

[comment]: <> (# sudo apt install unzip)

[comment]: <> (# unzip -o data.zip)

[comment]: <> (# sudo rm data.zip)

[comment]: <> (# Make sure you have edited extra-hosts.yaml to provide hostname mappings for combiners)

[comment]: <> (# Make sure you have edited client.yaml to provide hostname mappings for reducer)

[comment]: <> (sudo docker-compose -f docker-compose.yaml -f extra-hosts.yaml up --build)

[comment]: <> (```)

[comment]: <> (### Start prediction- global model serving)

[comment]: <> (We have made it possible to use the trained global model for prediction, to start the UI make sure that the FEDn-network is)

[comment]: <> (is started and run the flask app &#40;python predict/app.py&#41;)

[comment]: <> (```bash)

[comment]: <> (# prediction/)

[comment]: <> (python app.py)

[comment]: <> (```)


[comment]: <> (## License)

[comment]: <> (Apache-2.0 &#40;see LICENSE file for full information&#41;.)