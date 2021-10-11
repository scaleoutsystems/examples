import sys
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from data.read_data import read_data
import json
from sklearn import metrics
import os
import yaml
import numpy as np

def validate(model,data):
    print("-- RUNNING VALIDATION --", flush=True)

    # The data, split between train and test sets.

    # Training error (Client validates global model on same data as it trains on.)
    (x_train, y_train) = read_data(data, trainset=True)

    # Test error (Client has a small dataset set aside for validation)
    (x_test, y_test) = read_data(data, trainset=False)
     
    try:
        model_score = model.evaluate(x_train, y_train, verbose=0)
        print('Training loss:', model_score[0])
        print('Training accuracy:', model_score[1])

        model_score_test = model.evaluate(x_test, y_test, verbose=0)
        print('Test loss:', model_score_test[0])
        print('Test accuracy:', model_score_test[1])
        y_pred = model.predict(x_test)
        y_pred = np.argmax(y_pred, axis=1)
        clf_report = metrics.classification_report(y_test.argmax(axis=-1),y_pred)

    except Exception as e:
        print("failed to validate the model {}".format(e),flush=True)
        raise

    report = {
                "classification_report": clf_report,
                "training_loss": model_score[0],
                "training_accuracy": model_score[1],
                "test_loss": model_score_test[0],
                "test_accuracy": model_score_test[1],
            }

    print("-- VALIDATION COMPLETE! --", flush=True)
    return report

if __name__ == '__main__':

    with open('settings.yaml', 'r') as fh:
        try:
            settings = dict(yaml.safe_load(fh))
        except yaml.YAMLError as e:
            raise(e)

    from fedn.utils.kerashelper import KerasHelper
    helper = KerasHelper()
    weights = helper.load_model(sys.argv[1])

    from models.mnist_model import create_seed_model
    model = create_seed_model()
    model.set_weights(weights)

    report = validate(model,'../data/mnist.npz')

    with open(sys.argv[2],"w") as fh:
        fh.write(json.dumps(report))
