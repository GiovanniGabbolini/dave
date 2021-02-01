'''
Created on Fri Jan 17 2020

@author Giovanni Gabbolini
'''


import pandas as pd
import os
import gensim
import numpy as np
from src.data.check_file import check_file
# preprocessed_dataset_path = '~/Desktop/playlist-explanation/res/p'
preprocessed_dataset_path = 'res/p'
raw_dataset_path = 'res/r'
feature_path = f"{preprocessed_dataset_path}/features"
path_file_name_normalized_idf = preprocessed_dataset_path

_idf_correction = {}
_genres_graph = None


def playlist():
    df = pd.read_csv(os.path.join(preprocessed_dataset_path,
                                  'playlist.csv'))
    return df


def genres_graph():
    path = os.path.join(preprocessed_dataset_path, 'genres_graph.npy')
    check_file('genres_graph', path)
    global _genres_graph
    if _genres_graph == None:
        _genres_graph = np.load(os.path.join(preprocessed_dataset_path,
                                             'genres_graph.npy'), allow_pickle='TRUE').item()
    return _genres_graph


def the_chain():
    df = pd.read_csv(os.path.join(raw_dataset_path,
                                  'the_chain.csv'))
    return df


def track_album_artists_id(index=''):
    df = pd.read_csv(os.path.join(preprocessed_dataset_path,
                                  'track_album_artists_id.csv'))
    if index != '':
        df = df.set_index(index)
    return df


def word_embeddings():
    path = os.path.join(preprocessed_dataset_path, "glove_raw_1m")
    _word_embeddings = gensim.models.KeyedVectors.load(path, mmap='r')
    return _word_embeddings

# def idf_correction(key):
#     global _idf_correction
#     key = 'track_chorus'
#     if key not in _idf_correction:
#         if key == 'track_chorus':
#             _key = 'track_lyrics'
#             _idf_correction[key] = rdict('{}_{}'.format(
#                 save_normalized_idf.prefix_file_name, _key))
#         else:
#             _idf_correction[key] = rdict('{}_{}'.format(
#                 save_normalized_idf.prefix_file_name, key))
#     return _idf_correction[key]
