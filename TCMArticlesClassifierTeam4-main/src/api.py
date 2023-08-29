import pandas as pd
import json
import os
import tensorflow as tf


from embeddingDataSet import embed

model = tf.keras.models.load_model('case_report_classifier.h5')

def prepareVectors(path):
    dataset_json = []
    data = pd.read_csv(path, dtype=str)
    for i, row in data.iterrows():
        title = row['Title']
        abstract = row['Abstract']
        paperId = row['PaperId']
        # ensure that everything is right type
        if type(abstract) == type(title) == type(paperId) == str:
            dataset_json.append({'title': title,
                                 'abstract': abstract,
                                 'paper_id': paperId})
    print('EMBEDDING:', len(dataset_json))
    all_embeddings = embed(dataset_json)
    return all_embeddings

# def predictResult(path):
#     embeddings = prepareVectors(path)
#     print(model.predict(embeddings))