# Examples

This repository is (new) and will be hosting all the great examples that Scaleout provides its users for FEDn and STACKn.

Please read the README in each respective example for more information!


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
FEDn is framework agnostic but the examples each require whatever framework you see fit to use! And hence some dependencies are required. Install them by the following command:
```bash
$ pip install -r requirements.txt
``` 

4. Get the client config for your federation!
a) Start a reducer and combiner and base services by reading instructions in `https://github.com/scaleoutsystems/fedn.git/ or navigate to your pre-setup federation page (for example Scaleout Studio!)

5. Download the file and place it in the example folder of choice (replacing the existing client.yaml)

6. Start the client!
```bash
$ fedn run client -in client.yaml
```
7. Observe the federation structure have a new client associated using the _Network_ Monitor page in FEDn.

8. From here you can monitor, instruct and direct your federation.
(minimum requirement 1 client for examples).




