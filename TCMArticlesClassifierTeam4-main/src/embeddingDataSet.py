import os
import json
import requests
import pandas as pd

from typing import Dict, List

URL = "https://model-apis.semanticscholar.org/specter/v1/invoke"
MAX_BATCH_SIZE = 16

def chunks(lst, chunk_size=MAX_BATCH_SIZE):
    for i in range(0, len(lst), chunk_size):
        yield lst[i: i + chunk_size]


def embed(papers):
    embeddings_by_paper_id: Dict[str, List[float]] = {}
    for chunk in chunks(papers):
        # Allow Python requests to convert the data above to JSON
        response = requests.post(URL, json=chunk)
        if response.status_code != 200:
            raise RuntimeError("Sorry, something went wrong, please try later!")
        for paper in response.json()["preds"]:
            embeddings_by_paper_id[paper["paper_id"]] = paper["embedding"]


def embedData(dataDir, datasets):

    for dataset in datasets:
        dataset_json = []
        data = pd.read_csv(os.path.join(dataDir, 'rawCSVdata', '{}.csv'.format(dataset)), dtype=str)
        for i, row in data.iterrows():
            title = row['Title']
            abstract = row['Abstract']
            paperId = row['PaperId']
            # ensure that everything is right type
            if type(abstract) == type(title) == type(paperId) == str:
                dataset_json.append({'title': title,
                                     'abstract': abstract,
                                     'paper_id': paperId})
        #             doistr = '\r\n'.join(dataset_pids)
        print('EMBEDDING:', len(dataset_json))
        all_embeddings = embed(dataset_json)
        dataset_path = os.path.join(dataDir, 'embededData', f'{dataset} embeddings.json')
        with open(dataset_path, 'w') as f:
            json.dump(all_embeddings, f)