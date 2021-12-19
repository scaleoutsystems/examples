import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import yaml


def read_data(filename):

    """
    Helper function to read preprocessed data and split it.
    :return: train data
    """
    with open('settings.yaml', 'r') as fh:
        try:
            settings = dict(yaml.safe_load(fh))
        except yaml.YAMLError as e:
            raise (e)

    # Read the prepared and normlized data, where the features number is 36 and the output is 10 classes


    print("-- START READING DATA --")

    pkd = np.array(pd.read_csv(filename))
    print(pkd.shape)
    x = pkd[:, 1:37]
    y = pkd[:, 37:]
    _, X, _, Y  = train_test_split(x, y,test_size=settings['test_size'])

    # reshaped the input data for LSTM model
    X = X.reshape(X.shape[0], 1, X.shape[1])

    return X, Y


