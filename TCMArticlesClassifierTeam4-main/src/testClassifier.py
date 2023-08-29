import pandas as pd
import numpy as np
import pickle
import os
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout
from sklearn.preprocessing import LabelBinarizer
import sklearn.datasets as skds
from pathlib import Path

def testModel(dataDir, model):
    embededData_dir = os.path.join(dataDir, 'embededData')
    test_data_loc = os.path.join(embededData_dir, 'test embeddings.json')

    csvData_dir = os.path.join(dataDir, 'rawCSVdata')
    test = pd.read_csv(os.path.join(csvData_dir, 'test.csv'), dtype=str)
    test = test.drop_duplicates(subset=['PaperId'], keep='first')

    with open(test_data_loc, 'r') as f:
        test_embeddings = json.load(f)
    test = test[test['PaperId'].isin(test_embeddings)]

    assert test.shape[0] == len(test_embeddings)
    y_test = np.array([float(x) for x in test['tcm'].values]).T
    x_test = np.array([test_embeddings[PaperId] for PaperId in test.PaperId.tolist()])
    np.shape(y_test), np.shape(x_test)

    batch_size = 8
    score = model.evaluate(x_test,
                           y_test,
                           batch_size=batch_size,
                           verbose=1)

    print('Test accuracy:', score[1])