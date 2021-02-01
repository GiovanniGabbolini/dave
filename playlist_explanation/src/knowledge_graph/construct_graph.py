import networkx as nx
import matplotlib.pyplot as plt
from src.knowledge_graph.applicable_actions import ActionsSupplier
from src.data import data
import json


def construct_graph(song, supplier=None):
    """Given a dictionary representing a the initial song of a song ie the attributes provided
       by spotify, it constructs the directed knowledge graph associated with it.

       The graph is constructed automatically applying the functions in the folder
       src/features/specific and src/features/specific as they become applicable. This is handled by the supplier

       Every feature returns a dictionary. 
       It has always a value key.
       It can specify the type of node and edge we are creating. Otherwise, the node type is retrieve from annotation, the edge type is the func name
       Every other key will be enclosed in the node

       Every node in the graph share a common internal structure:
       - id: Unique string identifier. Constructed concatenating the functions applied to
             obtain that node to the name of the node from which that node comes from
       - type: Node type
       - value: Node value

       Every edge in the graph share a common internal structure:
       - type: Edge type
       - generating_function: Name of the feature that generated the node

       The type is the attribute used to search for the functions applicable

    Arguments:
        song {dict} -- 
        supplier {obj} -- Supplies which actions (features) can be applied to the graph nodes

    Returns:
        g {nx directed graph} --
    """
    g = nx.DiGraph()

    # Source dummy node
    g.add_node('source', type='source', value=id(g), id='source', graph=g)

    # Initialize the graph with the attributes contained in the song dictionary
    for k in song.keys():
        g.add_node(k, type=k, value=song[k], id=k, graph=g)
        g._node[k]['mergiable_id'] = craft_id_node_graph(g._node[k])
        g.add_edge('source', k, type='init', generating_function='init')

    action_supplier = ActionsSupplier() if supplier is None else supplier

    while True:

        # Retrieve the applicable functions
        actions = action_supplier.applicable_actions(g)

        if len(actions) == 0:
            break

        for action in actions:

            # Construct the actual dictionary to be passed to the function

            func = action[0]
            graph_keys = action[1]
            sig = action[2]

            func_args = list(sig.parameters.keys())

            assert len(graph_keys) == len(func_args)

            args = {}
            for idx in range(len(func_args)):
                if graph_keys[idx] == "DEFAULTVALUE":
                    assert sig.parameters[func_args[idx]].default is not inspect.Parameter.empty
                    args[func_args[idx]] = sig.parameters[func_args[idx]].default
                else:
                    args[func_args[idx]] = g.nodes()[graph_keys[idx]]

            # Call the function
            return_value = func(**args)

            if return_value is None:
                continue

            return_value = [return_value] if type(return_value) == dict else return_value
            for idx, v in enumerate(return_value):

                # Resolve node type, edge type and node value
                edge_type = v.pop('edge_type') if 'edge_type' in v else func.__name__
                node_type = v.pop('node_type') if 'node_type' in v else func.__annotations__['return']
                value_node = v.pop('value')

                assert type(edge_type) == str and type(node_type) == str

                # Craft node id
                id_starting_node = graph_keys[0]
                id_node = f"{id_starting_node}~{func.__name__}" if idx == 0 else f"{id_starting_node}~{func.__name__}-{idx}"

                generating_function = func.__name__

                # Add
                assert id_node not in g and id_starting_node in g
                g.add_node(id_node, value=value_node, type=node_type, id=id_node, graph=g, **v)
                g._node[id_node]['mergiable_id'] = craft_id_node_graph(g._node[id_node])
                g.add_edge(id_starting_node, id_node, type=edge_type, generating_function=generating_function)

    return g


def craft_id_node_graph(n):
    n_copy = n.copy()
    n_copy.pop('id')
    n_copy.pop('graph')
    s = ''
    keys = sorted(list(n_copy.keys()))
    for key in keys:
        s += f"~{key}:{n_copy[key] if type(n_copy[key])!=dict else json.dumps(n_copy[key], sort_keys=True)}"
    return s


if __name__ == "__main__":
    from src.features.read_feature_dataframe import read_feature_dataframe as rdf
    from src.data import data
    m = data.track_album_artists_id()
    track_name_df = rdf('track_name')
    df = track_name_df.merge(rdf('track_uri_spotify'),
                             how='left', on='tid').merge(m, how='left', on='tid').merge(rdf('artist_name'),
                                                                                        how='left', on='arid').merge(rdf('artist_uri_spotify'),
                                                                                                                     how='left', on='arid').merge(rdf('album_name'),
                                                                                                                                                  how='left', on='alid').merge(rdf('album_uri_spotify'), how='left', on='alid')
    assert len(df) == len(track_name_df)

    row = df[df.tid == 12]
    assert len(row) == 1

    d = {
        'track_uri_spotify': row.track_uri_spotify[0],
        'track_name': row.track_name[0],
        'artist_name': row.artist_name[0],
        'artist_uri_spotify': row.artist_uri_spotify[0],
        'album_name': row.album_name[0],
        'album_uri_spotify': row.album_uri_spotify[0],
    }

    # d = {
    #     'track_spotify_uri': 'spotify:track:0X9KRnbgET1DR1RObXVbXv',
    #     'track_name': 'Light On',
    #     'artist_name': 'Kaylee Bell',
    #     'artist_uri_spotify': 'spotify:artist:4J3TXBvAMckFbTxqxNYpDj',
    #     'album_name': 'Light On',
    #     'album_uri_spotify': 'spotify:album:6BBozn1t4tX500G1ZGjQeJ',
    # }

    g = construct_graph(d)

    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos)

    labels = {n: g.nodes()[n]['type'][0] for n in g.nodes()}
    nx.draw_networkx_labels(g, pos, labels=labels)
    nx.draw_networkx_edges(g, pos)
    plt.show()
