from src.knowledge_graph.io import load_sub_graphs, load_sub_graphs_generator
import random
from src.knowledge_graph.walk_graph import find_segues
import pandas as pd
from src.data import data
import logging
from src.utils.timing import tick, tock
from src.utils.musicbrainz_setup import musicbrainzngs_setup
from src.run.demo import add_scores_lines_description_to_segues
import numpy as np
from src.interestingness.interestingness_GB import interestingness
from tqdm import tqdm

_run_number = 0
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


def save_sub_graphs_that_match_the_chain_style():

    def _filter_by_genre(graph):
        edges = graph.out_edges('artist_name~artist_musicbrainz_id')
        for e in edges:
            n = graph.nodes()[e[1]]
            if n['type'] == 'musical_genre_musicbrainz_id' and graph[e[0]][e[1]]['generating_function'] == 'artist_genres':
                if n['value'] in ['fe12b346-a10e-450f-bf81-fa20894b5ea2',
                                  '58e325d5-54fd-4e98-b39a-3aa6bc319273',
                                  '911c7bbb-172d-4df8-9478-dbff4296e791',
                                  '797e2e85-5ffd-495c-a757-8b4079052f0e',
                                  '0e3fc579-2d24-4f20-9dae-736e1ec78798',
                                  '7d0c6a6b-5d56-4b1e-a8c7-e32194f246b9',
                                  'fe4ba6a1-9873-4fd0-a12b-a70c81818514',
                                  'a715278f-1580-409f-8078-4ffbc800e08b',
                                  '31be54b2-4d0c-42df-aa44-c496c7b4c3c3',
                                  '1b5e7b16-336b-473e-a364-5120413a9827']:
                    return True

        return False

    def _filter_by_country(graph):
        try:
            n = graph._node['artist_name~artist_musicbrainz_id~artist_based_in_area~area_country']
            if n['value'] in ['8a754a16-0027-3a29-b6d7-2b40ea0481ed']:
                return True
        except KeyError:
            pass

        try:
            n = graph._node['artist_name~artist_musicbrainz_id~artist_birth_place_area~area_country']
            if n['value'] in ['8a754a16-0027-3a29-b6d7-2b40ea0481ed']:
                return True
        except KeyError:
            pass

        return False

    sub_graphs_interestingness_generator = load_sub_graphs_generator(folder_name="sub_graphs_interestingness")
    eligible_subgraphs_test2 = []

    for generator in sub_graphs_interestingness_generator:
        for g in generator():

            if _filter_by_genre(g) and _filter_by_country(g):
                eligible_subgraphs_test2.append(g)

    np.save(f"{data.preprocessed_dataset_path}/sub_graphs_interestingness_candidates_test2/0", eligible_subgraphs_test2)


def run(interestingness_weights, text_kind, n_best_segues=10, random_seed=None):
    tick(__file__)
    global _run_number

    if _run_number == 0 and random_seed is not None:
        # Fix the sequence of sampled seed songs
        random.seed(random_seed)

    the_chain = pd.read_csv(f"{data.raw_dataset_path}/the_chain.csv")
    num_subgraphs_the_chain = len(the_chain)

    target = 1
    while True:
        _run_number += 1

        # The chain segue
        while True:
            idx = random.randint(1, num_subgraphs_the_chain-1)

            the_chain_line = the_chain.loc[idx].links
            try:
                the_chain_line = the_chain_line.replace('^ ', '').replace('^', '')
                break
            except AttributeError:
                continue

        if _run_number >= target:
            break
    # idx = 1265

    return segues(interestingness_weights, text_kind, idx, n_best_segues=n_best_segues)


def segues(interestingness_weights, text_kind, idx, n_best_segues=10):
    _setup()

    global _sub_graphs_candidates
    if _sub_graphs_candidates is None:
        _sub_graphs_candidates = load_sub_graphs(folder_name="sub_graphs_interestingness_candidates_test2")
    sub_graphs_the_chain_generator = load_sub_graphs_generator(folder_name="sub_graphs_the_chain")
    the_chain = pd.read_csv(f"{data.raw_dataset_path}/the_chain.csv")

    the_chain_line = the_chain.loc[idx].links
    try:
        the_chain_line = the_chain_line.replace('^ ', '').replace('^', '')
    except AttributeError:
        raise AttributeError(f"No segue is available for idx {idx}")

    l = []
    the_chain_graph = sub_graphs_the_chain_generator[(idx-1)//100]()[(idx-1) % 100]

    for g in tqdm(_sub_graphs_candidates):
        segues = find_segues(the_chain_graph, g)
        scores = interestingness(segues, **interestingness_weights)
        for segue, score in zip(segues, scores):
            l.append({**{'_score': score}, **segue})

    l = sorted(l, key=lambda e: e['_score'], reverse=True)
    best_segues = l[:n_best_segues]

    for i, segue in enumerate(best_segues):
        best_segues[i] = add_scores_lines_description_to_segues([segue], interestingness_weights, text_kind)[0]

    return {
        'track_name_1': the_chain.loc[idx-1].track_name,
        'artist_name_1': the_chain.loc[idx-1].artist_name,
        'track_name_2_the_chain': the_chain.loc[idx].track_name,
        'artist_name_2_the_chain': the_chain.loc[idx].artist_name,
        'track_name_2_dave': best_segues[0]['n2']['graph'].nodes()['track_name']['value'],
        'artist_name_2_dave': best_segues[0]['n2']['graph'].nodes()['artist_name']['value'],
        'the_chain_line': the_chain_line,
        'segues': best_segues,
    }


if __name__ == "__main__":
    save_sub_graphs_that_match_the_chain_style()
