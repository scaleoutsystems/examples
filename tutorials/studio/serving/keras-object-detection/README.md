# Serving object detection models

In this example we serve a number of open, pre-trained object detection models. We also deploy a Dash app that
lets a user upload an image and have it classified with all the deployed endpoints, as well as aggregate predicitons
in a bagging ensamble. This illustrates how to work with model and app serving in STACKn. 

## 1. Create STACKn  model objects 

The first step is to create STACKn model objects for each of the Keras models. 
In STACKn, create a new STACKn Project, then start a Jupyter Lab session mounting the `project-vol` as persistent volume. Once in Jupyter, start
a terminal and clone this repository into the `/work/project-vol` folder. Finally, open the notebook `Deploy.ipynb`
and follow the instructions to create model objects. 

## 2. Serve the models using the Tensorflow Serving application 

From the UI in the menu "serve", use the Tensorflow serving application to serve each model. This means that you should create three separete serving apps. Make sure to set _Permissions_ to `public`.

## 3. Configure the Dash application
For each served model, copy the endpoint url (by opening the application and copying the url). 
From the Jupyter Lab session, open and edit `app/endpoints.py` by replacing the urls with your served enpoints. 

## 4. Deploy the Dash application
From the UI, under the _Serve_ tab, use the 'Dash App' to deploy an application which uses the keras object detection models you have created. make sure to use the following settings: 

- **_Permissions_** : `Public`
- **_Persistent volume_**: `project-vol` 
- **_Deployment - Path to folder_**: `examples/tutorials/studio/serving/keras-object-detection/app`

## 5. Test the application 
Open the app by clicking on the open link and test the application, e.g. using the 'cat.jpg' image in this repostitory.

## 6. Publish the dash app
Under the serve tab, in the entry for your created dash-app, by clicking on the `publish` link you will make available your app to others collaborators who has access to the same Studio platform, from outside the context of your project/experiment. Once an app is published, it will then be avaible under the tab "Apps", in the "Catalogs" section in the top left corner of the Studio UI.
