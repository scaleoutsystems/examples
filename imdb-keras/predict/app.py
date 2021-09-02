from flask import Flask, render_template, request, json
from miniorepo import get_global_model, get_global_model_list
import keras as k
from models.imdb_model import create_seed_model
from io import BytesIO
import numpy as np

app = Flask(__name__)


@app.route('/')
def predict():
    try:
        global_model_list = get_global_model_list(bucket='fedn-models')
        return render_template('predict.html', global_model_list=global_model_list)
    except:
        raise Exception("Ops, Could not connect to bucket repo, make sure to run fedn network!")


def load_model(path):

    a = np.load(path)
    weights = []
    for i in range(len(a.files)):
        weights.append(a[str(i)])
    return weights


@app.route('/fedn_predict', methods=['POST'])
def imdb_predict():
    if request.method == 'POST':
        # upload seed file
        seed_model = request.form.get('model_type', 'nlp')
        global_model = request.form.get('global_model', '')
        text_review = request.form.get('input_value', '')
        model = get_global_model(global_model, bucket='fedn-models')
        model = BytesIO(model)
        weights = load_model(model)

        model = create_seed_model()
        model.set_weights(weights)

        # use model
        d = k.datasets.imdb.get_word_index()
        words = text_review.split()
        review = []
        for word in words:
            if word not in d:
                review.append(2)
            else:
                review.append(d[word] + 3)

        review = k.preprocessing.sequence.pad_sequences([review], truncating='pre', padding='pre', maxlen=100)
        prediction = model.predict(review)
        print("Prediction: (0 = negative, 1 = positive) = %0.4f" % prediction[0][0])

        result = prediction[0][0]
        return json.dumps(str(result))
    else:
        pass


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')