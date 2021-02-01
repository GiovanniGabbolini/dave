'''
Created on Thu Jan 16 2020

@author Giovanni Gabbolini
'''

import pandas as pd
import os
from src.data import data
import random
import math
from src.features.specific import *


def create_playlists(n=40, nrows_original_df=10000000, length_playlist_range=(15, 25), random_seed=0):
    """sample a number of playlists coming from a slice of the original interaction csv

    Keyword Arguments:
        n {int} -- [how many playlists to sample] (default: {20})
        nrows_original_df {int} -- [how many rows to consider in the original interaction csv] (default: {10000000})
        length_playlist_range {tuple} -- [range of admissible num of tracks for the playlist drawn] (default: {(10,20)})
        random_seed {int} -- (default: {0})
    """
    playlists = pd.read_csv(os.path.join(data.raw_dataset_path, 'spotify_recsys2018', 'interactions.csv'),
                            sep='\t', lineterminator='\r', nrows=nrows_original_df)
    random.seed(random_seed)
    df_to_concat = []
    for _ in range(n):
        while True:
            # on avg, a playlist has 70 tracks
            sample = random.randrange(math.ceil(nrows_original_df/70))
            playlist = playlists[playlists.pid == sample]
            if len(playlist) > length_playlist_range[0] and len(playlist) < length_playlist_range[1]:
                df_to_concat.append(playlist)
                break
    preproc_playlists = pd.concat(df_to_concat, axis=0)
    preproc_playlists.to_csv(os.path.join(
        data.preprocessed_dataset_path, 'playlist.csv'), index=False)


def create_track_album_artists_ids():
    tracks = pd.read_csv(os.path.join(
        data.raw_dataset_path, 'spotify_recsys2018', 'tracks.csv'), sep='\t', lineterminator='\r',)
    preproc_tracks = tracks.drop(
        ['track_uri', 'track_name', 'duration_ms'], axis=1)
    playlists = data.playlist()
    preproc_tracks_slice = preproc_tracks[preproc_tracks.tid.isin(
        playlists.tid)]
    preproc_tracks_slice.astype({'alid': 'int', 'arid': 'int', })
    preproc_tracks_slice = preproc_tracks_slice[['tid', 'alid', 'arid', ]]
    preproc_tracks_slice.to_csv(os.path.join(
        data.preprocessed_dataset_path, 'track_album_artists_id.csv'), index=False)


def album_name_spotifyuri():
    albums = pd.read_csv(os.path.join(
        data.raw_dataset_path, 'spotify_recsys2018', 'albums.csv'), sep='\t', lineterminator='\r',)
    track_album_artists_ids = data.track_album_artists_id()
    albums = albums[albums.alid.isin(
        track_album_artists_ids.alid)]
    albums = albums.rename(columns={'album_uri': 'album_uri_spotify'})
    create_feature(albums[['alid', 'album_name']])
    create_feature(albums[['alid', 'album_uri_spotify']])


def create_artist():
    artists = pd.read_csv(os.path.join(
        data.raw_dataset_path, 'spotify_recsys2018', 'artists.csv'), sep='\t', lineterminator='\r',)
    track_album_artists_ids = data.track_album_artists_id()
    artists = artists[artists.arid.isin(
        track_album_artists_ids.arid)]
    artists = artists.rename(columns={'artist_uri': 'artist_uri_spotify'})
    create_feature(artists[['arid', 'artist_uri_spotify']])
    create_feature(artists[['arid', 'artist_name']])


def create_track():
    tracks = pd.read_csv(os.path.join(
        data.raw_dataset_path, 'spotify_recsys2018', 'tracks.csv'), sep='\t', lineterminator='\r',)
    track_album_artists_ids = data.track_album_artists_id()
    tracks = tracks[tracks.tid.isin(
        track_album_artists_ids.tid)]
    tracks.track_name = tracks.track_name.str.strip()
    tracks = tracks.rename(
        columns={'track_uri': 'track_uri_spotify', 'duration_ms': 'track_duration_ms'})
    create_feature(tracks[['tid', 'track_uri_spotify']])
    create_feature(tracks[['tid', 'track_name']])
    create_feature(tracks[['tid', 'track_duration_ms']])


if __name__ == '__main__':
    create_playlists()
    create_track_album_artists_ids()
    create_artist()
    album_name_spotifyuri()
    create_track()
