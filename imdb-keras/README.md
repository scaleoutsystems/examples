# NLP- IMDB test project
This classic example of sentiment analysis is well suited both as a lightweight test when learning FEDn and developing on FEDn in psedo-distributed mode. A normal high-end laptop or a workstation should be able to sustain at least 5 clients. The example is also useful for general scalability tests in fully distributed mode. 


## Configure and start a client using cpu device
The easiest way to start clients for quick testing is to use shell script.The following 
shell script will configure and start a client on a blank Ubuntu 20.04 LTS VM:    


```bash
#!/bin/bash

# Install Docker and docker-compose
sudo apt-get update
sudo sudo snap install docker

# clone the nlp_imdb example
git clone https://github.com/aitmlouk/FEDn-client-imdb-keras.git
cd FEDn-client-imdb-keras

# if no available data, download it from archive
# wget https://archive.org/download/data_20210128/data.zip
# sudo apt install unzip
# unzip data.zip
# sudo rm data.zip

# Make sure you have edited extra-hosts.yaml to provide hostname mappings for combiners
# Make sure you have edited fedn-network.yaml to provide hostname mappings for reducer
sudo docker-compose -f docker-compose.10clients.yaml -f extra-hosts.yaml up --build
```

### Start prediction- global model serving
We have made it possible to use the trained global model for prediction, to start the UI make sure that the FEDn-network is
is started and run the flask app (python predict/app.py)
```bash
# prediction/
python app.py
```

### Configuring the tests
We have made it possible to configure a couple of settings to vary the conditions for the training. These configurations are expsosed in the file 'client/settings.yaml': 

```yaml 
# Parameters for local training
test_size: 0.25
batch_size: 32
epochs: 1
```

### Creating a compute package
To train a model in FEDn you provide the client code (in 'client') as a tarball. For convenience, we ship a pre-made package (nlp_imdb.tar.gz). Whenever you make updates to the client code (such as altering any of the settings in the above mentioned file), you need to re-package the code (as a .tar.gz archive) and copy the updated package to 'packages'.

```bash
tar -cf nlp_imdb.tar client
gzip nlp_imdb.tar
cp nlp_imdb.tar.gz packages/
```

## Creating a seed model
The baseline CNN-LSTM is specified in the file 'client/init_model.py'. This script creates an untrained neural network and serialized that to a file, which is uploaded as the seed model for federated training. For convenience we ship a pregenerated seed model in the 'seed/' directory. If you wish to alter the base model, edit 'client/models/imdb_model.py' and regenerate the seed file:
```bash
# client/models
python init_model.py 
```

## License
Apache-2.0 (see LICENSE file for full information).