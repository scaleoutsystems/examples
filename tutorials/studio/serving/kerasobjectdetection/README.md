# Serving object detection models

In this example we serve a number of open, pre-trained object detection models. We also deploy a Dash app that
lets a user upload an image and have it classified with all the deployed endpoints, as well as aggregate predicitons
in a bagging ensamble. This illustrates how to work with model and app serving in STACKn. 

## 1. Create STACKn  model objects 

The first step is to create STACKn model objects for each of the Keras models. 
In STACKn, create a new Project, then start a Jupyter Lab session mounting the project_volume. Start
a terminal, then clone this repository onto '/work/project_volume'. Then open the notebook 'Deploy.ipynb'
and follow the instructions to create model objects. 

## 2. Serve the models using the Tensorflow Serving application 

From the UI in the menu "serve", use the Tensorflow serving application to serve each model. Set 'Permissions' to 'public'. 

## 3. Configure the Dash application
For each served model, copy the endpoint url (by opening the application and copying the url). 
From the Jupyter Lab session, open and edit 'app/endpoints.py', replacing the urls with your served enpoints. 

## 4. Deploy the Dash application
From the UI, Serving menu, use the 'Dash App' application to deply the application. Use the settings: 

Permissions : Public
Persistent volume: project-vol 
deployment: examples/tutorials/studio/serving/kerasobjectdetection/app

## Test the application 
From the main 'Apps' menu, you can access and test the application, e.g. using the 'cat.jpg' image in this repostitory.  
