from src.knowledge_graph.io import load_sub_graphs_generator
from src.data import data
import pickle
from tqdm import tqdm
import json
import random
from src.knowledge_graph.compare_functions import *
from src.utils.utils_ngx_graph import father
import networkx as nx
from src.knowledge_graph.walk_graph import find_segues
from collections import defaultdict
import numpy as np
from src.features.specific import *
from src.features.common import *

"""
    Our interstingness
"""


_count = None


def load_count_sample():
    global _count
    if _count is None:

        with open(f"{data.preprocessed_dataset_path}/count_interestingness_GB.txt", 'rb') as f:
            _count = pickle.load(f)

        # Normalize segue_type_rarity score, as all the values are too close to 1.
        # We apply a logarithm normalization, so we:
        # 1) Compute log_2(1-rarity) for every value. This is an high number, in case rarity is close to 1, otherwise it is low;
        # 2) Consider the max over every value of the previous quantity (M);
        # 3) Divide log_2(1-rarity) by M, and get the normalized values.
        values = np.array(list(_count['segue_type_rarity'].values()))
        max_log_values = max(-np.log2(1-values))
        normalized = {k: -np.log2(1-v)/max_log_values for k, v in _count['segue_type_rarity'].items()}
        _count['segue_type_rarity'] = normalized

    return _count


def craft_id_node_graph(n):
    n_copy = n.copy()
    n_copy.pop('id')
    n_copy.pop('graph')
    s = ''
    keys = sorted(list(n_copy.keys()))
    for key in keys:
        s += f"~{key}:{n_copy[key] if type(n_copy[key])!=dict else json.dumps(n_copy[key], sort_keys=True)}"
    return s


def trace(n):
    tr = []
    while True:
        tr.insert(0, n['type'])
        father_n = father(n)
        if father_n is not None:
            tr.insert(0, n['graph'][father_n['id']][n['id']]['type'])
            n = father_n
        else:
            break
    return tr


def craft_segue_type(segue):
    segue_type = trace(segue['n1'])+[segue['compare_function']]+trace(segue['n2'])[::-1]
    return tuple(segue_type)


def save_count_sample():
    random.seed(39)

    count = {'node': {}}
    segue_type_count = defaultdict(int)

    sub_graphs_generator = load_sub_graphs_generator(folder_name="sub_graphs_interestingness")

    goal = 5000000
    done = 0
    with tqdm(total=goal) as pbar:
        while goal-done:

            indices = (random.randint(0, len(sub_graphs_generator)-1), random.randint(0, len(sub_graphs_generator)-1))
            batches = [sub_graphs_generator[idx]() for idx in indices]

            for _ in range(len(batches[0])*10):
                done += 1
                pbar.update(1)

                g1, g2 = tuple(random.choice(b) for b in batches)
                segues = find_segues(g1, g2)

                for segue in segues:
                    segue_type = craft_segue_type(segue)
                    segue_type_count[segue_type] += 1

    total_segues = sum(segue_type_count.values())
    segue_type_count = {k: v/total_segues for k, v in segue_type_count.items()}

    max_segue_type_count = max(segue_type_count.values())
    segue_type_count = {k: v/max_segue_type_count for k, v in segue_type_count.items()}

    segue_type_rarity = {k: 1-v for k, v in segue_type_count.items()}

    count['segue_type_rarity'] = segue_type_rarity

    # From sub_graphs, we construct a unique graph
    graph = nx.DiGraph()

    print('Merging subgraphs ...')
    for generator in tqdm(sub_graphs_generator):
        for g in generator():

            id_sub_graph = str(id(g.nodes()['source']['graph']))
            graph.add_node(id_sub_graph, type='source', value=id_sub_graph, id=id_sub_graph)

            # Element in queue represent nodes in the shape (id_node_in_subgraph, id_node_in_graph)
            q = [('source', id_sub_graph)]
            while True:

                if len(q) == 0:
                    break
                else:
                    node = q.pop(0)

                    edges = g.edges(node[0])
                    for edge in edges:

                        n = g.nodes()[edge[1]]

                        old_id = n['id']
                        new_id = craft_id_node_graph(n)

                        n.pop('id')
                        n.pop('graph')
                        graph.add_node(new_id, id=new_id, **n)

                        type_edge = g[node[0]][old_id]['type']
                        if (node[1], new_id) in graph.edges:
                            graph[node[1]][new_id]['type'].add(type_edge)
                        else:
                            graph.add_edge(node[1], new_id, type=set([type_edge]))

                        q.append((old_id, new_id))

    for n in graph._node.values():
        in_edges = graph.in_degree(n['id'])
        out_edges = graph.out_degree(n['id'])

        if n['type'] not in count['node']:
            count['node'][n['type']] = {}

        count['node'][n['type']][n['id']] = in_edges + out_edges

    for node_type in count['node'].keys():
        v = count['node'][node_type].values()
        count['node'][node_type]['__meadian__'] = np.median(list(v))

    with open(f"{data.preprocessed_dataset_path}/count_interestingness_GB.txt", 'wb') as f:
        pickle.dump(count, f, protocol=0)


def rarity_score(segue):
    count = load_count_sample()
    segue_type = craft_segue_type(segue)
    if segue_type in count['segue_type_rarity']:
        return count['segue_type_rarity'][segue_type]
    else:
        return -np.inf


def unpopularity_score(segue):

    def _popularity_node_to_source(node):
        pop_i = []
        while node['id'] != 'source':

            id_node = craft_id_node_graph(node)

            if node['type'] in count['node']:

                try:
                    node_edgeset = count['node'][node['type']][id_node]
                except KeyError:
                    node_edgeset = np.inf

                meadian_edgeset_actual_type = count['node'][node['type']]['__meadian__']
                pop_i.append(min(1, node_edgeset/meadian_edgeset_actual_type))

            else:
                return None

            node = father(node)

        return pop_i

    count = load_count_sample()

    pop_subpath_1 = _popularity_node_to_source(segue['n1'])
    pop_subpath_2 = _popularity_node_to_source(segue['n2'])
    if pop_subpath_1 is not None and pop_subpath_2 is not None:
        min_popularity = min(pop_subpath_1+pop_subpath_2)
        unpopularity = 1 - min_popularity
    else:
        unpopularity = -np.inf
    return unpopularity


def shortness_score(segue):
    length = 0
    for node in [segue['n1'], segue['n2']]:
        node = segue['n1']
        while True:
            node_father = father(node)
            generating_function = node['graph'][node_father['id']][node['id']]['generating_function']
            if generating_function == 'init':
                length += 1
                break
            func = getattr(globals()[generating_function], generating_function)
            length += 1 if 'entailed' not in func.__annotations__ else 0
            node = node_father
    shortness = 2/length
    return shortness


def interestingness(segues, rar_w, unpop_w, shortness_w):
    scores = []
    for segue in segues:
        rar = rarity_score(segue)
        unpop = unpopularity_score(segue)
        shortness = shortness_score(segue)
        score = rar_w*rar + unpop_w*unpop + shortness_w*shortness
        scores.append(score)
    return scores


def best_interestingness_weights():
    return {'rar_w': 0.4, 'unpop_w': 0.2, 'shortness_w': 0.4}


if __name__ == "__main__":
    save_count_sample()
