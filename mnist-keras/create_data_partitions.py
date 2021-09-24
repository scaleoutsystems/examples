import os
import sys
import numpy as np
from math import floor

def splitset(dataset, parts):
    """Partition data into "parts" partitions"""
    n = dataset.shape[0]
    local_n = floor(n/parts)
    result = []
    for i in range(parts):
        result.append(dataset[i*local_n: (i+1)*local_n])
    return np.array(result)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        nr_of_datasets = 10
    else:
        nr_of_datasets = int(sys.argv[1])

    package = np.load("data/mnist.npz")
    data = {}
    for key, val in package.items():
        data[key] = splitset(val, nr_of_datasets)

    print("CREATING {} PARTITIONS INSIDE {}/data/clients".format(nr_of_datasets, os.getcwd()))
    if not os.path.exists('data/clients'):
        os.mkdir('data/clients')

    for i in range(nr_of_datasets):
        if not os.path.exists('data/clients/{}'.format(str(i))):
            os.mkdir('data/clients/{}'.format(str(i)))
        np.savez('data/clients/{}'.format(str(i)) + '/mnist.npz',
                x_train=data['x_train'][i],
                y_train=data['y_train'][i],
                x_test=data['x_test'][i],
                y_test=data['y_test'][i])
    print("DONE")