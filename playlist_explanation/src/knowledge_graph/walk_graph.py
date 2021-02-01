from networkx.algorithms.simple_paths import _all_simple_paths_graph
import itertools
from src.knowledge_graph.segues_filtering import pre, post
from collections import defaultdict
from src.knowledge_graph.construct_graph import construct_graph
from src.knowledge_graph.resolve_compare_function import get_dict


def check_filters(segue, pre_filtering, post_filtering, d):
    if not pre_filtering(segue['n1'], segue['compare_function']) or not pre_filtering(segue['n2'], segue['compare_function']):
        return False

    if not post_filtering(segue['n1'], segue['n2'], segue['compare_function']):
        return False

    return True


def find_segues(g1, g2, pre_filtering=pre, post_filtering=post, d=get_dict()):
    """Find all segues joining an entity1 to an entity2.
    Entities are repesented as knowledge graphs g1 and g2

    Args:
        g1 (ngx graph)
        g2 (ngx graph)
        pre_filtering (dictionay, optional)
        post_filtering (dictionary, optional)
        d (dict, optional): Dictionary with, as keys, tuples of node types. As values, list of compare functions.
                            Two nodes of the types listed are compared according to the compare functions in list,
                            and, if judged so, segues are generated from such comparisons.
                            d is assumed to be symmetrical.

    Returns:
        list: List of dictionaries. Each dictionary represent a segues, shaped as:
              {
                  'n1': ngx node, node from g1 that connects with 'n2' in g2
                  'n2': ngx node, node from g2 that connects with 'n1' in g1
                  'value': segue-type specific value
                  'compare_function': compare function stating that such a connection exists
              }
    """
    # First, merges g1 and g2 in a unique graph.
    # Then, find segues as paths from the source node of g1 and the source node of g2.
    # Then, filters out undesired nodes
    # Finally, converts paths to the dictionary form.

    # Efficient structure where to store the merged graph
    g = defaultdict(set)

    # Map back a sequence of node ids in g to a list of nodes in g1 (dictionary 0) and g2 (dictionary 1)
    # A series of identical nodes in g can be mapped to more nodes in one of the starting graphs
    map_back = {'g1': defaultdict(list), 'g2': defaultdict(list)}

    # Tells whether an edge in g was from g1 or g2 or
    # if it was induced, i.e. resulting from the application of a compare functio to nodes from g1 and g2
    edges = {'g1': set(), 'g2': set(), 'induced': set()}

    # An induced edge is added as the result of the application of a compare function to two nodes
    # In induced_edges_infos we store these information
    induced_edges_infos = defaultdict(list)

    # Here we merge graphs

    # Every node in g1 and g2 is represented by a string, which is the conversion of its fields to text (mergiable_id)
    # This automatically implements the equal compare function, as equal nodes will converge into the same node in g
    compareble_nodes_with_equal = set([k[0] for k in d if 'equal' in [f.__name__ for f in d[k]]])
    for idx, addend in enumerate((g1, g2)):
        id_sub_graph = f"source_{idx}"
        stack = [((f"source_{idx}",), iter(addend['source']))]
        while stack:
            children = stack[-1]
            child = next(children[1], None)
            if child is None:
                stack.pop()
            else:
                child_id = addend.nodes()[child]['mergiable_id']
                child_id += f"__{idx}" if addend.nodes()[child]['type'] not in compareble_nodes_with_equal else ""

                if idx == 0:
                    g[children[0][-1]].add(child_id)
                    edges['g1'].add((children[0][-1], child_id))
                else:
                    g[child_id].add(children[0][-1])
                    edges['g2'].add((child_id, children[0][-1]))

                map_back[f'g{idx+1}'][children[0]+(child_id,)].append(child)
                stack.append((children[0]+(child_id,), iter(addend[child])))

    # Now we add edges stemming for compare functions different from equal
    compareble_nodes_without_equal = [k for k, v in d.items() if 'equal' not in [f.__name__ for f in d[k]]]
    # Every key in d is a tuple of types, so broadcasting to type_1 and type_2
    for type_1, type_2 in compareble_nodes_without_equal:

        nodes_type_1 = [g1.nodes()[node_id] for node_id in g1.nodes() if g1.nodes()[node_id]['type'] == type_1]
        nodes_type_2 = [g2.nodes()[node_id] for node_id in g2.nodes() if g2.nodes()[node_id]['type'] == type_2]

        for compare_function in [f for f in d[(type_1, type_2)] if f.__name__ != 'equal']:

            nodes_type_1_filtered = [n for n in nodes_type_1 if pre(n, compare_function)]
            nodes_type_2_filtered = [n for n in nodes_type_2 if pre(n, compare_function)]

            for n1, n2 in itertools.product(nodes_type_1_filtered, nodes_type_2_filtered):
                result = compare_function(n1, n2)
                if result['outcome'] == True:

                    # Add the edge
                    id_1 = f"{n1['mergiable_id']}__0" if n1['type'] not in compareble_nodes_with_equal else n1['mergiable_id']
                    id_2 = f"{n2['mergiable_id']}__1" if n2['type'] not in compareble_nodes_with_equal else n2['mergiable_id']
                    g[id_1].add(id_2)
                    edges['induced'].add((id_1, id_2))

                    # Store the result of the compare function application in a dictionary
                    result.pop('outcome')
                    result['compare_function'] = compare_function.__name__
                    induced_edges_infos[(n1['id'], n2['id'])].append(result)

    # Find paths in graph
    paths = list(_all_simple_paths_graph(g, 'source_0', {'source_1'}, 50))

    # Convert paths to dictionary-shaped segues
    segues = []

    # Find out which is the last node that belongs to g1 and which is the first that belongs to g2
    # middle_leg is len==2 tuple which has as values such information
    for j, path in enumerate(paths):
        for idx, leg in enumerate(zip(path, path[1:])):
            if leg not in edges['g1']:
                middle_leg = leg
                break

        if middle_leg in edges['g2']:
            # Compare function == equal
            for id_1, id_2 in itertools.product(map_back['g1'][tuple(path[0:idx+1])], map_back['g2'][tuple(path[idx:][::-1])]):

                segue = {'n1': g1._node[id_1],
                         'n2': g2._node[id_2],
                         'value': g1._node[id_1]['value'],
                         'compare_function': 'equal'}

                if check_filters(segue, pre_filtering, post_filtering, d) == True:
                    segues.append(segue)

        elif middle_leg in edges['induced']:
            # Compare function != equal
            for id_1, id_2 in itertools.product(map_back['g1'][tuple(path[0:idx+1])], map_back['g2'][tuple(path[idx+1:][::-1])]):

                candidated_segues = iter([{**{'n1': g1._node[id_1], 'n2': g2._node[id_2]}, **induced_edge_infos}
                                          for induced_edge_infos in induced_edges_infos[(id_1, id_2)]])

                for segue in candidated_segues:
                    if check_filters(segue, pre_filtering, post_filtering, d) == True:
                        segues.append(segue)

        else:
            raise ValueError(
                "Conceptual error: when finding middle_leg, it is assumed that it will be in either in edges['g2'] or in edges['induced']")

    return segues
