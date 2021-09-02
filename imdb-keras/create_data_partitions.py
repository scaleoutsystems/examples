import os
import sys
import pandas as pd
from math import floor


def import_data(test_ratio):
    """ Download data. """
    data = pd.read_csv('https://archive.org/download/train_202109/train.csv')
    data = data.sample(frac=1).reset_index(drop=True)
    data.to_csv("data.csv", index=False)
    num_test = int(test_ratio*data.shape[0])
    testset = data[:num_test]
    trainset = data[num_test:]
    return trainset, testset


def splitset(dataset, parts):
    n = dataset.shape[0]
    local_n = floor(n/parts)
    result = []
    for i in range(parts):
        result.append(dataset[i*local_n: (i+1)*local_n])
    return result


if __name__ == '__main__':

    if len(sys.argv) < 2:
        nr_of_datasets = 10
    else:
        nr_of_datasets = sys.argv[1]

    trainset, testset = import_data(0.1)
    print('trainset', len(trainset))
    print('testset', len(trainset))

    trainsets = splitset(trainset, nr_of_datasets)
    testsets = splitset(testset, nr_of_datasets)

    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/clients'):
        os.mkdir('data/clients')

    for i in range(nr_of_datasets):
        if not os.path.exists('data/clients/{}'.format(str(i))):
            os.mkdir('data/clients/{}'.format(str(i)))
        trainsets[i].to_csv('data/clients/{}'.format(str(i)) + '/train.csv', index=False)
        testsets[i].to_csv('data/clients/{}'.format(str(i)) + '/test.csv', index=False)