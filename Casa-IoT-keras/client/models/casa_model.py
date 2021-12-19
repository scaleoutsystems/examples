import tensorflow
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM

# Create an initial LSTM Model
def create_seed_model():
    model = Sequential()
    model.add(LSTM(100, input_shape=(1,36)))
    model.add(keras.layers.Dense(72, activation='relu'))
    model.add(keras.layers.Dense(50, activation='relu'))
    model.add(keras.layers.Dense(36, activation='relu'))
    model.add(keras.layers.Dense(28, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])
    return model
