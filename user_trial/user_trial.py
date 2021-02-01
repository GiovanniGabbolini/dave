from playlist_explanation.src.data.data import preprocessed_dataset_path, raw_dataset_path
from playlist_explanation.src.interestingness.interestingness_GB import best_interestingness_weights
from playlist_explanation.src.run.test_2 import segues
import glob
import random
import json
import re
import os
import pandas as pd
from playlist_explanation.src.log.log_mongo import log_mongo
from profanity import profanity


def save_segues():
    interestingness_weights = best_interestingness_weights()
    the_chain = pd.read_csv(f"{raw_dataset_path}/the_chain.csv")
    j = 0

    for idx in range(len(the_chain)):

        try:
            v = segues(interestingness_weights, 'short', idx, n_best_segues=1)
        except Exception:
            continue

        j += 1

        segue_dave = v['segues'][0]
        segue_dave.pop('n1')
        segue_dave.pop('n2')
        segue_dave.pop('_score')

        d = {
            'idx': idx,
            'seed_song': {
                'track_name': v['track_name_1'],
                'artist_name': v['artist_name_1'],
            },
            'song_the_chain': {
                'track_name': v['track_name_2_the_chain'],
                'artist_name': v['artist_name_2_the_chain'],
            },
            'song_dave': {
                'track_name': v['track_name_2_dave'],
                'artist_name': v['artist_name_2_dave'],
            },
            'segue_the_chain': v['the_chain_line'] if j != 4195 else "From smoke to smokey...",
            'segue_dave': v['segues'][0],
        }

        with open(f"{preprocessed_dataset_path}/user_trial/{j}.json", 'w') as fp:
            json.dump(d, fp)


def save_user_trial_segue_sample():
    """Takes a sample of json files saved by save_segues() and save
    it into another folder, to be used for drawing it during the user trial.

    We'd like to pose a limit on the number of different segues that we show, so
    that there would be also a limit on the number of segues we'll have to
    label manually.

    We choose to take a sample of 200 segues.
    """

    sample_size = 200

    folder_src = f"{preprocessed_dataset_path}/user_trial"
    folder_dst = f"{preprocessed_dataset_path}/user_trial_sample"
    number = len(glob.glob1(folder_src, "*.json"))

    # filter out profanity
    pool = []
    from tqdm import tqdm
    for j in tqdm(range(1, number+1)):

        with open(f"{folder_src}/{j}.json") as fp:
            d = json.load(fp)

        if not profanity.contains_profanity(d['seed_song']['artist_name']) and \
                not profanity.contains_profanity(d['seed_song']['track_name']) and \
                not profanity.contains_profanity(d['song_the_chain']['artist_name']) and \
                not profanity.contains_profanity(d['song_the_chain']['track_name']) and \
                not profanity.contains_profanity(d['song_dave']['artist_name']) and \
                not profanity.contains_profanity(d['song_dave']['track_name']) and \
                not profanity.contains_profanity(d['segue_dave']['line']) and \
                not profanity.contains_profanity(d['segue_the_chain']):
            pool.append(j)

    # sampling
    random.seed(42)
    sample = random.sample(pool, sample_size)

    for j in sample:

        with open(f"{folder_src}/{j}.json") as fp:
            d = json.load(fp)

        with open(f"{folder_dst}/{j}.json", 'w') as fp:
            json.dump(d, fp)


def draw(n=1):
    """Returns a random sample without replacement of segues from The Chain and Dave to be compared.
    The sample has size n
    An elem in the sample consists of a seed song, the segue + second song from the chain, the segue + second song from dave

    In particular every d in r has fields:
    - idx: index of the seed song as it comes from the chain
    - seed_song, song_the_chain, song_dave: dictionary with track_name and artist_name
    - segue_the_chain: the segue in string format
    - segue_dave: the segue in string format

    Returns:
        list
    """
    folder = f"{preprocessed_dataset_path}/user_trial_sample"
    candidates = [x for x in os.listdir(folder) if re.match(r'\d+.json', x)]

    # random segue
    js = [int(s.split('.')[0]) for s in random.sample(candidates, n)]

    r = []
    for j in js:
        with open(f"{folder}/{j}.json") as fp:
            d = json.load(fp)
            d['idx_user_trial_folder'] = j
        r.append(d)

    return r


def save_answers(d, collection='answers'):
    d.pop('_id', None)
    d = {k: v.replace('</br>', '').strip() if type(v) == str else v for k, v in d.items()}
    log_mongo(collection, d, db_name='pilot')


if __name__ == "__main__":
    save_user_trial_segue_sample()
