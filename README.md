# Examples

This repository hosts examples that Scaleout provides its users for FEDn and STACKn.

Please read the README in each respective example for more information!

## Starting a native client (FEDn)

1. Create a virtual environment and activate it
```bash
$ python3 -m venv env
$ source env/bin/activate
```

2. Install the fedn client
```bash
$ pip install fedn
```

3. Pick your example.
```bash
$ cd "mnist-keras"  #for example!
```

4. Setup dependencies for the specific example

Each client/example require an execution context, and thus dependencies are required. Install them by the following command:
```bash
$ pip install -r requirements.txt
``` 

5. Check the README of the example you are working on for instructions on/if to prepare local data sources.
  
6. Get the client config for your federation!
The config file client.yaml is obtained by downloading from the _Network_  page of the Reducer. Download the file and place it in the example folder of choice (replacing the existing client.yaml)

7. Start the client. 
```bash
$ fedn run client -in client.yaml
```
Check that the federation has a new client associated at the _Network_  page in FEDn.

You are now ready to start training the federated model (_Control_  page of the Reducer.)
(Repeat above steps as needed to deploy additional clients, minimum requirement 1 client for examples).
