# STACKn/Studio quick tests

This tutorial is intended as quick tests/examples to get started using STACKn / Studio. It assumes access to an already deployed STACKn instance. 

_______________________
### Known Issues
1. Occasionally you might see an error page reading something like "Suspicious activity...". This is due to a known bug, and not due to some suspicious activity. Click "Back" in your browser and reload the page, and it should work again.
___________________________

General preparation: Download the Jupyter Notebooks from this repository, or be prepared to Git clone the repo or files as needed.

# MNIST

Purpose is to build and deploy a simple neural network.

Steps:

1. Create a "STACKn Default" project (wait a bit and refresh the page until all apps are created and available)
2. Start a new lab session (_Compute -> New -> Lab_) on the main Overview page. Name can be anything, select "project-vol" as Persistent Volume and leave the rest as defaults. 
3. Upload the _mnist_example_tf_serving.ipynb notebook_ to your project folder in labs (project-vol). Alternatively `wget https://raw.githubusercontent.com/scaleoutsystems/examples/main/tutorials/studio/quickstart/mnist_example_tf_serving.ipynb` in the Jupyter terminal.
4. Run the notebook up to (and including) the cell where the model is saved (`tf.saved_model.save...`).
5. In the Jupyter terminal (from your project folder, 'models' should be a subdirectory)

    5.1 `stackn create object mnist -r minor`

    5.2 `stackn get objects` (check that the model is listed)

6. Go back to the STACKn interface, go to Serve and deploy the model as a Tensorflow model:
    
    6.1 Click _Create_ in _Tensorflow Serving_
    
    6.2 Choose a name, set _Model_ to the model you just created and leave the rest as defaults
    
    6.3 A Tensorflow Serving service will pop up in the top of the window. Check logs to verify that it has deployed, (look for 'Entering the event loop ...') by clicking the folder icon.

7. Get the endpoint (right click the _Open_ link), paste it into the Jupyter notebook and call the endpoint to verify that it works.


# AML

1. Create a STACKn default project, or create a volume in your existing project.

2. Create a new lab session, then launch a terminal.

3. Clone the AML repository to your volume: 

    3.1 cd your-project-volume
   
    3.2 git clone https://github.com/scaleoutsystems/aml-example-project.git

4. Create a model object in STACKn:

    4.1 cd aml-example-project

    4.2 Create a tar archive of the relevant folders: 
    ```tar czvf ../aml-model.tar.gz src models requirements.txt setup.py helpers.py``` 
    (we do this to avoid including the big "dataset" directory)

    4.3 ```stackn create object aml -f ../aml-model.tar.gz -r minor```

5. Deploy the model with the "Python Model Deployment" app.
6. Get the endpoint, check the logs, and go to the notebook "notebooks/predict.ipynb" in the repository. Paste your URL, and make a prediction.

# PyTorch

1. You can either clone this repo or just download locally the file called `vgg11_scripted.mar`
2. Create a "STACKn Default" project (wait a bit and refresh the page until all apps are created and available).
3. In your STACKn default project, open your Minio instance (by clicking on the Minio name link).
4. Once you are redirected to the Minio UI, perform the log in by entering the access key and secrets (**tips**: they are available under the settings tab of the Minio app).
5. Create a bucket, say "pytorch", and Upload the `vgg11_scripted.mar` model archive.
6. Deploy the model with the _PyTorch Serve_ app (under the _Serve_ tab); the endpoint permissions should be "_public_" and the volume should be your Minio volume. Path to model store is your bucket name (e.g. "pytorch"). List of models can be left empty (then, by default, all models in the directory will be deployed). Few steps later you will use your PyTorch endpoit URL for running predictions.
7. Create a new _volume_ for a Dash app, say "dash-vol".
8. Go to the _Develop_ tab and launch a VSCode instance where you mount your newly created volume (e.g. "dash-vol") as a persisten volume for VSCode.
9. In your VSCode instance clone this repository and open the sub-folder _dash-test_. (**tips**: it should be possible to clone this sub-folder only with git).
10. Go under the _Serve_ tab and copy your PyTorch endpouint URL. (**tips**: right-click on the "_open_" link and copy the URL)
11. In VSCode, go to the _dash-test_ folder and update line of 97 the `app.py` file with your PyTorch endpoint URL. **Note**: since the model name is "vgg11_scripted", so the URL should be for example: ```https://torch-serve.studio.local.stackn.dev/predictions/vgg11_scripted```
12. Deploy the dash app with the related _Dash Deployment_ component (under _Serve_ tab): _Permissions_ can be either "public" or "project"; mount the created volume (e.g."dash-vol"); _Path to folder_ should be relative to your volume and it should be the "dash-test" sub-folder clone or downloaded in the previous step; finally and importantly, let _Debug deployment_ be "False".
13. Open the Dash App UI (by clickin on the "_open_" link)
14. Test the app! You can use "ball.jpeg" which you can find in this repository or any other image.
15. Last but not least, have fun!

# Transformers example project

1. Clone the repo onto a volume: https://github.com/scaleoutsystems/transformers-example-project
2. In the repository directory, run ```stackn create object afbert -r minor```.
3. Deploy the model with "Python Model Deployment". It takes a long time for this model to initialize, so keep checking the logs until it is available. That the "State" is "Running" does not mean that the model has initialized, only that the container is running.
4. Copy the endpoint url, paste it in the appropriate place in the "predict" notebook in the repository, and run the prediction.

# FEDn MNIST

>Preparations: It helps to have a local copy of the FEDn repository available. Clone or download it from https://github.com/scaleoutsystems/fedn. You will also use deploy-fedn-mnist.ipynb and mnist-predict.ipynb from this repository (https://github.com/scaleoutsystems/test-examples)

### Setting a reducer and combiner in STACKn
1. Create a new project using the FEDn Project template.

2. Wait for all resources to start. Reload the page until you see a running Jupyter Notebook under "Compute", a "FEDn Combiner" under FEDn and a "FEDn Reducer" under FEDn.

3. To train a model in FEDn you provide the client code as a tarball. For convenience, we ship a pre-made package (the 'client' folder in the FEDn repository) that defines what happens on the client side during training and validation, as well as some settings.
- Open the link to the FEDn Reducer in a new tab
- Click the '/context' link and upload mnist.tar.gz from https://github.com/scaleoutsystems/fedn/tree/master/test/mnist-keras/package

4. The baseline model (a CNN) is specified in the file 'client/init_model.py'. This script creates an untrained neural network and serializes that to a file, which is uploaded as the seed model for federated training. For convenience we ship a pregenerated seed model in the 'seed/' directory. If you wish to alter the base model, edit 'init_model.py' and regenerate the seed file
- Click 'History' in the left menu
- Click 'Choose file:' and upload seed.npz from https://github.com/scaleoutsystems/fedn/tree/master/test/mnist-keras/seed

5. Go to 'Network' in the left menu and check that there is a combiner listed under 'Combiners', with 0 'Active clients'

### Setting up a local client
We will now set up a separated client that will attach to the combiner. This should be done on a Linux/Unix machine with Docker.

1. Clone the FEDn repo
```bash
git clone --depth 1 --single-branch --branch=develop https://github.com/scaleoutsystems/fedn.git
```
2. Edit the fedn-network.yaml in fedn/test/mnist-keras/. Change the __discover_host__ to the URL of the FEDn Reducer (e.g. copy it from the browser URL bar, omit the scheme and trailing slash, so for instance: ```reducer-fedn-mnist-hbr-0491.studio.safespring-prod.stackn.dev```). Change the __discover_port__ to __443__.

3. Rebuild the client
```bash
docker build -t client-local:latest .
```

4. Run the Docker image
```bash
docker run -it -v /absolute/path/to/fedn/test/mnist-keras/data:/app/data client-local:latest fedn run client -in fedn-network.yaml
```

### Run federated training 
Now it's time to run a few federated training rounds. Go to the Reducer web UI. 
1. Go to 'Control' in the left menu.
2. Run a few rounds of training by expanding the list after 'Run rounds:', selecting 3 and then 'Submit'
3. Go to 'History' in the left menu and refresh until a new model name appears.
4. Go to 'Dashboard' in the left menu to see stats about the training rounds as they complete. Refresh the page to update with results from more training rounds.

This completes the setup and training of a federated model!

### Publish and serve the model as an API
To make the model useful it will be saved as a Tensorflow model and deployed in a serving container, as a publicly available web service.

1. Go to the STACKn Overview page.
2. Open the Jupyter service (open 'Lab' in a new tab).
3. Open a Jupyter Terminal and clone the FEDn repo
```bash
cd project-volume
git clone --depth 1 --single-branch --branch=main https://github.com/scaleoutsystems/examples.git
```
5. Save the model as a Tensorflow model. 
- Upload __deploy-fedn-mnist.ipynb__ from this repo to __examples/mnist-keras/client__.
- Open it and replace the model name with the most recent model name from 'minio-vol/fedn-models'
- Run all cells to save the model.
- A new object is created in STACKn via the Python API: ```stackn.create_object('fedn-mnist', release_type="minor")```

6. The model was created as a Tensorflow model, so it can now be deployed using the Tensorflow serving app. 
- Go to STACKn, select Serve in the left menu.
- Click 'Create' under 'Tensorflow Serving'
- Name: can be anything
- Select your model.
- Leave all other settings as their defaults
- Click 'Create'

7. Wait for the container to deploy. You can check the log (via the folder icon) for 'Entering the event loop'.

8. When deployed, copy the link to the endpoint by right-clicking 'Open' and copy link address. 

9. Test the serving by uploading __mnist-predict.ipynb__ to the 'project-volume' (in Jupyter) and pasting the endpoint link in the request.post call.

10. Run all cells to make a public (over the internet call) to the model and get a prediction from your federated model back!
