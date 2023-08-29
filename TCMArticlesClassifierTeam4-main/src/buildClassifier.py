import pandas as pd
import numpy as np
import os
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout


def buildModel(dataDir):
    embededData_dir = os.path.join(dataDir, 'embededData')
    dev_data_loc = os.path.join(embededData_dir, 'dev embeddings.json')
    train_data_loc = os.path.join(embededData_dir, 'train embeddings.json')

    csvData_dir = os.path.join(dataDir, 'rawCSVdata')
    train = pd.read_csv(os.path.join(csvData_dir, 'train.csv'), dtype=str)
    dev = pd.read_csv(os.path.join(csvData_dir, 'dev.csv'), dtype=str)
    print(train.shape)

    with open(train_data_loc, 'r') as f:
        train_embeddings = json.load(f)
    with open(dev_data_loc, 'r') as f:
        dev_embeddings = json.load(f)

    train = train.drop_duplicates(subset=['PaperId'], keep='first')
    dev = dev.drop_duplicates(subset=['PaperId'], keep='first')
    print(train.shape)

    dev = dev[dev['PaperId'].isin(dev_embeddings)]
    train = train[train['PaperId'].isin(train_embeddings)]
    print(train.shape)
    print(train.columns)

    assert train.shape[0] == len(train_embeddings)
    assert dev.shape[0] == len(dev_embeddings)

    y_train = np.array([float(x) for x in train['tcm'].values]).T
    x_train = np.array([train_embeddings[PaperId] for PaperId in train.PaperId.tolist()])
    y_dev = np.array([float(x) for x in dev['tcm'].values]).T
    x_dev = np.array([dev_embeddings[PaperId] for PaperId in dev.PaperId.tolist()])

    batch_size = 8
    model = Sequential()

    model.add(Dense(16, input_shape=(768,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    model.add(Dense(8))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.build()
    model.summary()

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    history = model.fit(x_train,
                        y_train,
                        validation_data=(x_dev, y_dev),
                        batch_size=batch_size,
                        epochs=6,
                        verbose=1,
                        )

    model.save('case_report_classifier.h5')
