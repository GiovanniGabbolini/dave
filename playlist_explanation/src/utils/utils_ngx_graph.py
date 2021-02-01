
def successors_iter(node):

    def successors_iter_recursive(graph, node_id):
        successors = list(graph.successors(node_id))
        if len(successors) == 0:
            return [[graph.nodes()[node_id]]]
        else:
            aggregate = []
            for n in successors:
                l = successors_iter_recursive(graph, n)
                for sub_l in l:
                    aggregate.append([graph.nodes()[node_id]]+sub_l)
            return aggregate

    l = [e[1:] for e in successors_iter_recursive(node['graph'], node['id']) if len(e) > 1]
    return l


def predecessors_iter(node):
    l = []
    while True:
        node = father(node)
        if node is None:
            break
        else:
            l.insert(0, node)
    return l


def album_name(g):
    return g.nodes()['album_name']['value'] if 'album_name' in g else ''


def artist_name(g):
    return g.nodes()['artist_name']['value'] if 'artist_name' in g else ''


def artist_id(g):
    return g.nodes()['artist_name~artist_musicbrainz_id']['value'] if 'artist_name~artist_musicbrainz_id' in g else ''


def track_name(g):
    return g.nodes()['track_name']['value'] if 'track_name' in g else ''


def track_chorus(g):
    return g.nodes()['track_name~track_lyrics~track_chorus']['value'] if 'track_name~track_lyrics~track_chorus' in g.nodes() else '',


def artist_type(g):
    """Returns either person, group, choir, orchestra or character
    """
    if 'artist_name~artist_musicbrainz_id~artist_type' in g.nodes():
        return g.nodes()['artist_name~artist_musicbrainz_id~artist_type']['value'].lower()
    else:
        return 'person'


def artist_gender(g):
    """Returns either male or female
    """
    if 'artist_name~artist_musicbrainz_id~artist_gender' in g.nodes():
        return g.nodes()['artist_name~artist_musicbrainz_id~artist_gender']['value'].lower()
    else:
        return 'male'


def artist_band_end_activity_year(g):
    """Returns either an integer or None
    """
    if 'artist_name~artist_musicbrainz_id~artist_band_end_activity_year' in g.nodes():
        return g.nodes()['artist_name~artist_musicbrainz_id~artist_band_end_activity_year']['value'].lower()
    else:
        return None


def artist_solo_end_activity_year(g):
    """Returns either an integer or None
    """
    if 'artist_name~artist_musicbrainz_id~artist_solo_end_activity_year' in g.nodes():
        return g.nodes()['artist_name~artist_musicbrainz_id~artist_solo_end_activity_year']['value'].lower()
    else:
        return None


def father(node):
    """Return the father of a node

    Arguments:
        node {ngx graph node} --

    Returns:
        ngx graph node -- None if no father
    """
    for k in node['graph'].predecessors(node['id']):
        return node['graph'].nodes()[k]
