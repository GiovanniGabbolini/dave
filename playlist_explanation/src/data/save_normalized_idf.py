'''
Created on Sat Feb 01 2020

@author Giovanni Gabbolini
'''


from src.text_processing.compute_normalized_idf import compute_normalized_idf
import numpy as np
from src.data.data import preprocessed_dataset_path
import os
import pandas as pd
prefix_file_name = 'normalized_idf'
path_file_name = preprocessed_dataset_path


def save_normalized_idf(source):
    if source == 'track_name':
        df = pd.read_csv(os.path.join(data.raw_dataset_path, 'tracks.csv'),
                         sep='\t', lineterminator='\r', usecols=['track_name'])
        corpus = [d for d in df['track_name'].values]
    elif source == 'album_name':
        df = pd.read_csv(os.path.join(data.raw_dataset_path, 'albums.csv'),
                         sep='\t', lineterminator='\r', usecols=['album_name'])
        corpus = [d for d in df['album_name'].values]
    elif source == 'artist_name':
        df = pd.read_csv(os.path.join(data.raw_dataset_path, 'artists.csv'),
                         sep='\t', lineterminator='\r', usecols=['artist_name'])
        corpus = [d for d in df['artist_name'].values]
    elif source == 'track_lyrics':
        df = pd.read_csv(os.path.join(data.raw_dataset_path,
                                      'tracks_lyrics_raw.csv'), usecols=['lyrics'])
        corpus = [d for d in df['lyrics'].values if type(d) == str]
    else:
        raise Exception('source type not recognized')
    d = compute_normalized_idf(corpus)
    np.save(os.path.join(path_file_name,
                         '{}_{}.npy'.format(prefix_file_name, source)), d)


if __name__ == "__main__":
    # save_normalized_idf('track_name')
    # save_normalized_idf('album_name')
    # save_normalized_idf('artist_name')
    save_normalized_idf('track_lyrics')
