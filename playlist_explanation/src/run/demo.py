"""
Created on Fri Feb 21 2020

@author Giovanni Gabbolini
"""
from src.features.specific import *
import logging
from src.utils.timing import tick, tock
from src.text_processing.preprocess_track_name import preprocess_track_name
import concurrent.futures
from src.knowledge_graph.construct_graph import construct_graph
from src.knowledge_graph.walk_graph import find_segues
from src.interestingness.interestingness_GB import rarity_score, unpopularity_score, shortness_score
from src.canned_texts.segue_canned_texts import segue_canned_texts
import numpy as np
from itertools import repeat


def _setup():
    # logger set up
    logger = logging.getLogger("root")
    if not logger.hasHandlers():
        logger.setLevel(logging.WARNING)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    logger = logging.getLogger("root.demo.build_track_object.timing")
    logger.setLevel(logging.DEBUG)

    logger = logging.getLogger("root.knowledge_graph")
    logger.setLevel(logging.ERROR)

    logger = logging.getLogger("root.features.timing")
    logger.setLevel(logging.ERROR)


def add_scores_lines_description_to_segues(segues, interestingness_weights, text_kind):
    segues_decorated = []

    for idx, segue in enumerate(segues):
        rarity = rarity_score(segue)
        unpopularity = unpopularity_score(segue)
        shortness = shortness_score(segue)
        score = interestingness_weights['rar_w']*rarity + \
            interestingness_weights['unpop_w']*unpopularity + \
            interestingness_weights['shortness_w']*shortness
        d = {
            'score': score,
            'rarity': rarity,
            'unpopularity': unpopularity,
            'shortness': shortness,
            'idx': idx,
        }
        segues_decorated.append({**d, **segue})

    with concurrent.futures.ThreadPoolExecutor() as ex:
        lines = ex.map(segue_canned_texts, segues, repeat(text_kind))

    for s, l in zip(segues_decorated, lines):
        s['line'] = l

    # Sorting
    segues_decorated = sorted(segues_decorated, key=lambda e: e['score'], reverse=True)

    # The description is only needed for the first segue
    segues_decorated[0]['explanation'] = segue_canned_texts(segues[segues_decorated[0]['idx']], 'description')

    # Formatting
    for r in segues_decorated:
        r['score'] = str(round(r['score'], 5)) if r['score'] != -np.inf else 'NaN'
        r['rarity'] = str(round(r['rarity'], 5)) if r['rarity'] != -np.inf else 'NaN'
        r['unpopularity'] = str(round(r['unpopularity'], 5)) if r['unpopularity'] != -np.inf else 'NaN'
        r['shortness'] = str(round(r['shortness'], 5)) if r['shortness'] != -np.inf else 'NaN'
        del r['idx']

    return segues_decorated


def run(tracks, interestingness_weights, text_kind):
    """returns the textual link linking tracks beloning to the the playlist retrieved before
       the tracks have all the info needed for the algorithm to run
    """
    _setup()

    tick(f"{__file__}total")
    tick(f"{__file__}total_graph")

    # tracks = tracks[:2]

    tracks_filtered_keys = []
    for t in tracks:
        d = {
            'track_name': preprocess_track_name(t['track_name']),
            'album_name': preprocess_track_name(t['album_name']),
            'artist_name': t['artist_name'],
            'track_uri_spotify': t['track_uri_spotify'],
            'album_uri_spotify': t['album_uri_spotify'],
            'artist_uri_spotify': t['artist_uri_spotify'],
        }
        tracks_filtered_keys.append(d)

    # multi-processing
    with concurrent.futures.ThreadPoolExecutor() as ex:
        graphs = list(ex.map(construct_graph, tracks_filtered_keys))

    # single-processing
    # graphs = []
    # for t in tracks_filtered_keys:
    #     tick(f"{__file__}single")
    #     graphs.append(construct_graph(t))
    #     logging.getLogger("root.demo.build_track_object.timing").debug(
    #         f"Took {tock(__file__+'single')} to build graph.")

    logging.getLogger("root.demo.build_track_object.timing").debug(
        f"Took {tock(__file__+'total_graph')} to construct graphs")

    story = []
    for g1, g2 in zip(graphs, graphs[1:]):
        segues = find_segues(g1, g2)

        if len(segues) > 0:
            result = add_scores_lines_description_to_segues(segues, interestingness_weights, text_kind)
        else:
            result = [{'line': f"The next track is <i>{g2.nodes()['track_name']['value']}</i>, by <i>{g2.nodes()['artist_name']['value']}</i>.",
                       'explanation': "We did not find a connection between the previous track and this one.",
                       'score': 'NaN',
                       }]

        story.append(result)

    logging.getLogger("root.demo.build_track_object.timing").debug(
        f"Took {tock(__file__+'total')} to complete the procedure")
    return story
