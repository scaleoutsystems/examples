## Starting a native client
If you want to start a native client there is a very quick way to get started!

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
FEDn is framework agnostic, but each example requires an environment with the frameworks used for that project. Install the needed dependencies using the following command:
```bash
$ pip install -r requirements.txt
``` 

5. Get the client config for your federation.
  a) Start a FEDn network with a reducer, combiner and base services by following the instructions `https://github.com/scaleoutsystems/fedn.git/, or 
  b) Navigate to a pre-setup federation page (for example Scaleout Studio)

6. Download the network configuration file from the "Network" view in the FEDn UI, then place it in the example folder of choice (replacing the existing client.yaml)

7. Start the client!
```bash
$ fedn run client -in client.yaml
```
8. Observe the federation structure displaying a new client associated on the _Network_ page in FEDn.

9. From here you can monitor, instruct and direct your federation.
(minimum requirement 1 client for examples).



