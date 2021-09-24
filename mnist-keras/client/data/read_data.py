import numpy as np
import tensorflow as tf

def read_data(path, trainset=True):
    """ Helper function to read and preprocess data for training with Keras. """

    pack = np.load(path)

    if trainset:
        X = pack['x_train']
        y = pack['y_train']
    else:
        X = pack['x_test']
        y = pack['y_test']

    classes = range(10)

    X = X.astype('float32')
    X = np.expand_dims(X,-1)
    X /= 255
    y = tf.keras.utils.to_categorical(y, len(classes))
    return  (X, y)
