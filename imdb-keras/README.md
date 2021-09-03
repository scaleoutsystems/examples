# IMDB example - Keras version
This classic example of sentiment analysis is well suited both as a lightweight test when learning FEDn and developing on FEDn in psedo-distributed mode. A normal high-end laptop or a workstation should be able to sustain at least 5 clients. The example is also useful for general scalability tests in fully distributed mode. 

### Local training and test data
To download and prepare the partitioned dataset (creates 10 partitions) in ./data/clients/0 etc:
``` bash
python create_data_partitions.py
```

## Configuring the Reducer  
Navigate to 'https://localhost:8090' (or the url of your Reducer) and follow instructions to upload the compute package in 'package/package.tar.gz' and the initial model in 'initial_model/initial_model.npz'. 

## Attaching a client to the federation

1. First, download 'client.yaml' from the Reducer 'Network' page, and replace the content in your local 'client.yaml'. 
2. Start a client. Here there are different options (see below): 
    - Docker 
    - docker-compose
    - [Native client (OSX/Linux)](https://github.com/scaleoutsystems/examples/tree/main/how-tos/start-native-fedn-client)

#### Docker
1. Build the image

``` bash
docker build . -t imdb-client:latest
```

2. Start a client (edit the path of the volume mounts to provide the absolute path to your local folder) and change the data partition in clients folder.
```
docker run -v /absolute-path-to-this-folder/data/clients/0:/app/data -v /absolute-path-to-this-folder/client.yaml:/app/client.yaml --network fedn_default imdb-client fedn run client -in client.yaml 
```
(Repeat above steps as needed to deploy additional clients).

#### docker-compose
To start 10 clients: 

```bash
docker-compose -f docker-compose.yaml -f private-network.yaml up 
```
> If you are connecting to a Reducer part of a distributed setup or in Studio, you should omit 'private-network.yaml'. 

#### Native client on OSX/Linux
The compute package assumes that the local dataset in in a folder 'data' in the same folder as you start the client. Make a new folder and copy the data partition you want to use into data:
```bash
cp data/clients/0/*.csv data/
```
Then [follow the instructions here](https://github.com/scaleoutsystems/examples/tree/main/how-tos/start-native-fedn-client) to start the client. 

### Start training 
When clients are running, navigate to the 'Control' page of the Reducer to start the training. 

### Configuring the client
We have made it possible to configure a couple of settings to vary the conditions for the training. These configurations are expsosed in the file 'settings.yaml': 

```yaml 
# Parameters for local training
test_size: 0.25
batch_size: 32
epochs: 1
```

## Creating a compute package
Whenever you make updates to the client code (such as altering any of the settings in the above mentioned file), you need to re-package the compute package:

```bash
tar -czvf package.tar.gz client
```
To clear the system and set a new compute package, see: https://github.com/scaleoutsystems/fedn/blob/master/docs/FAQ.md

For an explaination of the compute package structure and content: https://github.com/scaleoutsystems/fedn/blob/develop/docs/tutorial.md
 
## Creating a new initial model
The baseline CNN-LSTM is specified in the file 'client/init_model.py'. This script creates an untrained neural network and serializes that to a file.  If you wish to alter the initial model, edit 'init_model.py' and 'models/imdb_model.py' then regenerate the initial model file (install dependencies as needed, see requirements.txt):

```bash
python init_model.py 
```

## License
Apache-2.0 (see LICENSE file for full information).
