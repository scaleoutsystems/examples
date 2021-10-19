import io
import base64
import requests
import time

import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from requests.api import request

import tensorflow as tf
from tensorflow.keras.preprocessing import image

import numpy 
import collections 


from endpoints import endpoints

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
    {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Scaleout - Image Classifier"
server = app.server

app.layout = html.Div([
    dbc.Nav(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.A('Keras Object Detection',
                                   href='/', className='navbar-brand')
                        ], className='navbar-header'), html.Div(
                        [
                            html.Ul(
                                [
                                    html.Li(html.A('Scaleout Systems', href='https://www.scaleoutsystems.com/')), html.Li(
                                        html.A('Github', href='https://github.com/scaleoutsystems/examples'))
                                ], className='nav navbar-nav')
                        ], className='collapse navbar-collapse')
                ], className='container')
        ], className='navbar navbar-inverse navbar-fixed-top'),
    html.Div(
        [
            html.H1('Keras Object Detection',
                    className='text-center'),
            html.P('Demo of served Keras object detection applications',
                   className='text-center'),
            html.Hr(),
            html.Div(
                [
                    dcc.Upload(id='upload-image', children=html.Div(['Drag and Drop or ', html.A('Select File')]),
                               style={
                        'width': '98%',
                        'height': '100x',
                        'lineHeight': '60px',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                        # Allow multiple files to be uploaded
                        multiple=False
                    ),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div(id="loading-output")
                    ),
                    html.Hr(),
                ], className='container')
        ], className='jumbotron'),
    html.H2('Prediction', className='text-center'),
    dbc.Row([
        dbc.Col([
            html.Div(id='output-image-upload',
                     className="container text-center")
        ]),
        dbc.Col([
            html.Hr(),
            html.Div(id='output-image-result',
                     className="container text-center bg-info")
        ])
    ]),
], className="container")


@app.callback(Output("loading-output", "children"),
              Output('output-image-upload', 'children'),
              Output('output-image-result', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    print("In: update output", flush=True)

    image_html = []

    pred_res = []
    ensemble_pred = []
    try:
        content_type, content_string = list_of_contents.split(',')

        print(content_type)
        contentb64_decode = base64.b64decode(content_string)
        file_obj = io.BytesIO(contentb64_decode)
        with open('temp.jpg','wb') as fh:
            fh.write(file_obj.getbuffer())
            fh.flush()

        aggregated_prediction = collections.Counter()
        num_predictions = 0
        all_predictions = {}
        for model, url in endpoints.items():
            prediction = predict(model,url)

            for pred in prediction:
                key = pred[1]
                prob = pred[2]
                try: 
                    aggregated_prediction[key] += prob
                except:
                    aggregated_prediction[key] = prob
                num_predictions += 1
 
            pred_res.append(html.Div(
                [
                    #html.B(key, style={'font-weight': 'bold'}),
                    html.Span(["{}: {}".format(model, prediction)])
                ], style={'font-size': '20px'}))

        for key, value in aggregated_prediction.items():
            aggregated_prediction[key] = value/float(num_predictions)

        ensemble_pred.append(html.Div(
            [
                #html.B(key, style={'font-weight': 'bold'}),
                html.Span(["Aggregated prediction: {}".format(aggregated_prediction)])
            ], style={'font-size': '20px'}))



    except Exception as err:
        print("No image.")
        print(err)

    return image_html, pred_res

def predict_request(url,inp):

    # If you are running locally with self signed certificate, then CHANGE the verify variable to False
        verify = True
        try:
            print("Predicting")
            tic = time.time()
            res = requests.post(url, json=inp)
            toc = time.time()-tic
        except Exception as e:
            print(e)

        return {'time': toc, 'predicted_prob': res.json()['outputs']}

def predict(model, url):
    img_path='temp.jpg'

    if model == 'resnet50':
        from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = numpy.expand_dims(x, axis=0)
        x = preprocess_input(x)
        inp = {"inputs": x.tolist()}
        res = predict_request(url,inp)
        print(res['time'])
        prediction = decode_predictions(numpy.array(res['predicted_prob']),top=3)[0]
    elif model == 'xception':
        from tensorflow.keras.applications.xception import preprocess_input, decode_predictions
        img = image.load_img(img_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = numpy.expand_dims(x, axis=0)
        x = preprocess_input(x)
        inp = {"inputs": x.tolist()}
        res = predict_request(url,inp)
        print(res['time'])
        prediction = decode_predictions(numpy.array(res['predicted_prob']),top=3)[0]
    elif model == 'inceptionv3':
        from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
        img = image.load_img(img_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = numpy.expand_dims(x, axis=0)
        x = preprocess_input(x)
        inp = {"inputs": x.tolist()}
        res = predict_request(url,inp)
        print(res['time'])
        prediction = decode_predictions(numpy.array(res['predicted_prob']),top=3)[0]
    else: 
        prediction = None

    return prediction



if __name__ == '__main__':
    app.run_server(debug=True)