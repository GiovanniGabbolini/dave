from src.knowledge_graph.io import load_sub_graphs_generator
import random
from src.knowledge_graph.walk_graph import find_segues
import pandas as pd
from src.data import data
from src.utils.timing import tick, tock
import logging
from src.utils.musicbrainz_setup import musicbrainzngs_setup
from src.run.demo import add_scores_lines_description_to_segues

_sub_graphs = None
_num_subgraphs_the_chain = None


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


def run(interestingness_weights, text_kind):
    tick(__file__)
    _setup()

    global _sub_graphs
    global _num_subgraphs_the_chain
    if _sub_graphs is None:
        _sub_graphs = load_sub_graphs_generator(folder_name="sub_graphs_the_chain")
        _num_subgraphs_the_chain = sum(len(generator()) for generator in _sub_graphs)

    the_chain = pd.read_csv(f"{data.raw_dataset_path}/the_chain.csv")

    # The chain segue
    while True:
        idx = random.randint(1, _num_subgraphs_the_chain-1)

        the_chain_line = the_chain.loc[idx].links
        try:
            the_chain_line = the_chain_line.replace('^ ', '').replace('^', '')
            break
        except AttributeError:
            continue

    g1_the_chain = _sub_graphs[(idx-1)//100]()[(idx-1) % 100]
    g2_the_chain = _sub_graphs[idx//100]()[idx % 100]

    # Dave segue
    segues_found = find_segues(g1_the_chain, g2_the_chain)

    if len(segues_found) > 0:
        segues = add_scores_lines_description_to_segues(segues_found, interestingness_weights,text_kind)
    else:
        segues = [{'line': f"The next track is <i>{the_chain.loc[idx].track_name}</i>, by <i>{the_chain.loc[idx].artist_name}</i>.",
                   'explanation': "We did not find a connection between the previous track and this one.",
                   'score': 'NaN',
                   }]

    print(f"Test 1 total time: {tock(__file__)}")
    return {
        'track_name_1': the_chain.loc[idx-1].track_name,
        'artist_name_1': the_chain.loc[idx-1].artist_name,
        'track_name_2': the_chain.loc[idx].track_name,
        'artist_name_2': the_chain.loc[idx].artist_name,
        'the_chain_line': the_chain_line.replace('^ ', '').replace('^', ''),
        'segues': segues,
    }


if __name__ == "__main__":
    run({
        'rar_w': 0.33,
        'unpop_w': 0.33,
        'shortness_w': 0.34,
    })
