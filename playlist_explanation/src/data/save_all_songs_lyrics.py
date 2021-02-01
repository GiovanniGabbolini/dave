
'''
Created on Tue Feb 04 2020

@author Giovanni Gabbolini
'''


import pandas as pd
import os
from src.data import data
from bounded_pool_executor import BoundedProcessPoolExecutor as PoolExecutor
from src.features.specific.track_year_lyrics_instrumental import get_genius_info
import numpy as np
from src.utils.Logger import Logger
import requests


def save_all_songs_lyrics():
    """retrieves the lyrics for every song in the raw song csv and save them
    """
    if os.path.isfile(os.path.join(
            data.raw_dataset_path, 'idx_tracks_lyrics_raw.npy')):
        read_idx = np.load(os.path.join(
            data.raw_dataset_path, 'idx_tracks_lyrics_raw.npy'), allow_pickle=True)
    else:
        read_idx = 0
    chunksize = 50000
    df_artists = pd.read_csv(os.path.join(data.raw_dataset_path, 'artists.csv'),
                             sep='\t', lineterminator='\r', usecols=['arid', 'artist_name'])

    logger = Logger('save_all_lyrics_song', True)
    logger.write_line(
        'Starting to search lyrics from row: {}'.format(read_idx*chunksize))

    for idx, df_tracks in enumerate(pd.read_csv(os.path.join(data.raw_dataset_path, 'tracks.csv'), chunksize=chunksize, sep='\t', lineterminator='\r', usecols=['tid', 'arid', 'track_name'])):
        if idx <= read_idx:
            continue
        df = df_tracks.merge(df_artists, how='left')
        df = df.drop(['arid'], axis=1)
        lyrics = [None]*len(df)
        tid_rescaled = range(len(df))

        try_again = True
        while try_again:
            try:
                with PoolExecutor(max_workers=300) as executor:
                    for tid, l, _, _ in executor.map(get_genius_info, zip(tid_rescaled, df.track_name, df.artist_name)):
                        lyrics[tid] = l
                try_again = False
            except (requests.exceptions.RequestException, ValueError) as e:
                logger.write_line('Error caught!')
                logger.write_line(e)

        df_to_save = pd.DataFrame({'tid': df.tid.values, 'lyrics': lyrics})
        if idx == 0:
            df_to_save.to_csv(os.path.join(
                data.raw_dataset_path, 'tracks_lyrics_raw.csv'), index=False)
        else:
            df_to_save.to_csv(os.path.join(
                data.raw_dataset_path, 'tracks_lyrics_raw.csv'), mode='a', index=False)
        logger.write_line(
            'Done with searching lyrics until row: {}'.format(idx*chunksize))
        np.save(os.path.join(
                data.raw_dataset_path, 'idx_tracks_lyrics_raw.npy'), [idx])


if __name__ == "__main__":
    save_all_songs_lyrics()
