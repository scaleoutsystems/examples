# Deploy FEDn on OSX/Linux 

pip install fedn 

Create folder and change owner to user: 

``` bash
sudo mkdir /app
sudo mkdir /app/client/package
sudo chown <user> /app
```

## Reducer


Create a deployment directory (owned by user)
```bash
mkdir fedn-deploy
cd fedn-deploy
mkdir certs
```

Create a file 'settings-reducer.yaml' with the following content: 

```yaml

network_id: fedn-test-network

control:
  state: idle
  helper: keras

statestore:
  type: MongoDB
  mongo_config:
    username: fedn_admin
    password: password
    host: localhost
    port: 6534

storage:
  storage_type: S3
  storage_config:
    storage_hostname: localhost
    storage_port: 9000
    storage_access_key: fedn_admin
    storage_secret_key: password
    storage_bucket: fedn-models
    context_bucket: fedn-context
    storage_secure_mode: False 
    
 ```
 Start the Reducer: 
 
 ```bash
 fedn run reducer -n reducer  --init=settings-reducer.yaml
 ```
 
 ## Combiner
 
 Create a file 'settings-combiner.yaml': 
 
 ```yaml
network_id: fedn-test-network
controller:
    discover_host: localhost
    discover_port: 8090
    token: token

combiner:
    name: combiner
    host: localhost
    port: 12080
    max_clients: 30
 ```
 
 Start the combiner: 
 ```bash
 fedn run combiner -in settings-combiner.yaml
```

Proceed to select and example and start clients, for example the [MNIST getting-started example using Keras/Tensorflow] (https://github.com/scaleoutsystems/examples/tree/main/mnist-keras) 
 