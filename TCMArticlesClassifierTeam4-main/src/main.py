import os

from embeddingDataSet import embedData
from buildClassifier import buildModel
from testClassifier import testModel
from tensorflow import keras

if __name__ == '__main__':
    datasets = ['train','dev','test']
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataDir = os.path.join(dir, 'data')

    # getData(dataDir, datasets)
    # embedData(dataDir, datasets)

    model = keras.models.load_model('./case_report_classifier.h5')
    testModel(dataDir, model)

