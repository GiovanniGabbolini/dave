from playlist_explanation.src.knowledge_graph.io import load_sub_graphs, load_sub_graphs_generator
import random
from playlist_explanation.src.knowledge_graph.walk_graph import find_segues
from playlist_explanation.src.knowledge_graph.construct_graph import construct_graph
import pandas as pd
from playlist_explanation.src.data import data
from playlist_explanation.src.data.the_chain import get_last_element_the_chain
import logging
from playlist_explanation.src.utils.timing import tick, tock
from playlist_explanation.src.utils.musicbrainz_setup import musicbrainzngs_setup
from playlist_explanation.src.run.demo import add_scores_lines_description_to_segues
import numpy as np
from playlist_explanation.src.interestingness.interestingness_GB import interestingness, best_interestingness_weights
from tqdm import tqdm

_sub_graphs_candidates = None


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
    logger = logging.getLogger("root.knowledge_graph.resolve_compare_function")
    logger.setLevel(logging.ERROR)
    musicbrainzngs_setup()


def run(interestingness_weights, text_kind, d=None, n_best_segues=10):
    """Run this test

    Args:
        interestingness_weights (dict): dict with keys: rar_w, unpop_w, shortness_w
        text_kind (str): either 'line', 'description', 'short'
        n_best_segues (int, optional): Defaults to 10.
        d: seed song, formatted as {
            "track_name":
            "artist_name:"
            }
           If none, it will fetch from the internet, as the last record on the chain.
    Returns:
        dict
    """
    tick(__file__)
    _setup()

    global _sub_graphs_candidates
    if _sub_graphs_candidates is None:
        _sub_graphs_candidates = load_sub_graphs(folder_name="sub_graphs_interestingness_candidates_test2")

    last_element_the_chain = get_last_element_the_chain() if d is None else d
    the_chain_graph = construct_graph(last_element_the_chain)

    # Dave segue
    l = []
    for g in tqdm(_sub_graphs_candidates):
        segues = find_segues(the_chain_graph, g)
        scores = interestingness(segues, **interestingness_weights)
        for segue, score in zip(segues, scores):
            l.append({**{'_score': score}, **segue})

    l = sorted(l, key=lambda e: e['_score'], reverse=True)

    best_segues = l[:n_best_segues]

    for i, segue in enumerate(best_segues):
        best_segues[i] = add_scores_lines_description_to_segues([segue], interestingness_weights, text_kind)[0]

    print(f"Test 3 total time: {tock(__file__)}")
    return {
        'track_name_1': last_element_the_chain['track_name'],
        'artist_name_1': last_element_the_chain['artist_name'],
        'track_name_2': best_segues[0]['n2']['graph'].nodes()['track_name']['value'],
        'artist_name_2': best_segues[0]['n2']['graph'].nodes()['artist_name']['value'],
        'segues': best_segues,
    }


if __name__ == "__main__":
    track_name=input("Insert song name: ")
    artist_name=input("Insert artist name: ")
    d = run(best_interestingness_weights(), 'short',
            d={"track_name": track_name, "artist_name": artist_name})
    print(f"{track_name} by {artist_name}")
    print(f"^ {d['segues'][0]['line']}")
    print(f"{d['track_name_2']} by {d['artist_name_2']}")