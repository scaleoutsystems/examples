# MNIST test project
This classic example of hand-written text recognition is well suited both as a lightweight test when learning FEDn and developing on FEDn in psedo-distributed mode. A normal high-end laptop or a workstation should be able to sustain at least 5 clients. The example is also useful for general scalability tests in fully distributed mode. 

> Note that this file descibes how to configure an alliance for a particular FedML-model and how to attach clients. We here assume that a FEDn network is aleady up and running. If this is not the case, start here: https://github.com/scaleoutsystems/fedn/blob/master/README.md

## Configuring the Reducer  
Navigate to 'https://localhost:8090' (or the url of your Reducer) and follow instructions to upload the compute package in 'package/mnist.tar.gz' and the initial model in 'initial_model/initial_model.npz'. 

## Setting up a client

### Provide local training and test data
This example is provided with the mnist dataset from https://s3.amazonaws.com/img-datasets/mnist.npz in 'data/mnist.npz'.
To make testing flexible, each client subsamples from this dataset upon first invokation of a training request, then cache this subsampled data for use for the remaining lifetime of the client. It is thus normal that the first training round takes a bit longer than subssequent ones.  

## Download or configure client.yaml
Download client.yaml from the Reducer 'Network' page,  and replace the content in 'client.yaml'.
The client.yaml file  contains all the required information for a client to connect to a federation.

## Start the client
The easiest way to start clients for quick testing is by using Docker. We provide a docker-compose template for convenience:

```bash
docker-compose up -f ../config/private-network.yaml --scale client=2 
```
to start a client and attach it to the local private-network where you run reducer and combiner.


> Note that this assumes that a FEDn network is running in pseudo-distributed mode (see separate deployment instructions) and uses the default service names. If you are connecting to a reducer part of a distributed setup, first, edit 'fedn-network.yaml' to provide IP address to the reducer. Also provide an 'extra_hosts.yaml' file with combiner:host mappings (edit the file according to your network)

```bash
docker-compose -f docker-compose.yaml -f extra-hosts.yaml up 
```

When clients are running, navigate to 'localhost:8090/start' to start the training. 

### Configuring the tests
We have made it possible to configure a couple of settings to vary the conditions for the training. These configurations are expsosed in the file 'settings.yaml': 

```yaml 
# Number of training samples used by each client
training_samples: 600
# Number of test samples used by each client (validation)
test_samples: 100
# How much to bias the client data samples towards certain classes (non-IID data partitions)
bias: 0.7
# Parameters for local training
batch_size: 32
epochs: 1
```

