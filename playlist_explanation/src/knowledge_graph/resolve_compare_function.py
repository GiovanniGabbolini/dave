from src.knowledge_graph.compare_functions import *
from src.utils.utils_ngx_graph import father
import copy
"""
_dict says with which function compare couple of nodes, based on their type.
It can be indexed recursively, eg: 
                                {
                                    (t1,t2):{
                                        (t3, t4): [func1],
                                        (t5, t6): [func2],
                                    }
                                }

A compare function tells wheter there is a path from two nodes or not.
Visually, the equal compare function is true if two nodes are the same, so there is no arc connecting the two, they are simply the same node
The other compare function, if true, mean that there is a path among the two nodes. This happens when their value is different,
but still they have a relationships that can lead to a path among the two

Whereas nested structure are allowed, we assume to have a plain _dict, with key tuples of types that index a list of compare functions.
If we would like to avoid the association of nodes based on the type of the parents, we can discard the segues using segue filternings in the walk_graph function 
"""

# _dict is simmetric!

# ('word', 'word'): [equal.equal, related_word_semantics_phrase.related_word_semantics_phrase, ],

_dict = {
    ('lemma', 'lemma'): [equal.equal, ],
    ('synset', 'synset'): [equal.equal, ],
    ('word', 'word'): [equal.equal, ],
    ('stem', 'stem'): [equal.equal, ],
    ('place_musicbrainz_id', 'place_musicbrainz_id'): [equal.equal, ],
    ('event_musicbrainz_id', 'event_musicbrainz_id'): [equal.equal, ],
    ('recording_musicbrainz_id', 'recording_musicbrainz_id'): [equal.equal, ],
    ('release_musicbrainz_id', 'release_musicbrainz_id'): [equal.equal, ],
    ('work_musicbrainz_id', 'work_musicbrainz_id'): [equal.equal, ],
    ('release_group_musicbrainz_id', 'release_group_musicbrainz_id'): [equal.equal, ],
    ('artist_musicbrainz_id', 'artist_musicbrainz_id'): [equal.equal, ],
    ('phonetical_representation', 'phonetical_representation'): [equal.equal, ],
    ('artist_gender', 'artist_gender'): [equal.equal, ],
    # ('token_phrase', 'token_phrase'): [same_word_different_sense_phrase.same_word_different_sense_phrase, ],
    # ('track_name', 'track_lyrics_without_section_tags'): [uncommon_words.uncommon_words],
    # ('album_name', 'track_lyrics_without_section_tags'): [uncommon_words.uncommon_words],
    # ('artist_name', 'track_lyrics_without_section_tags'): [uncommon_words.uncommon_words],
    # ('track_lyrics_without_section_tags', 'track_name'): [uncommon_words.uncommon_words],
    # ('track_lyrics_without_section_tags', 'album_name'): [uncommon_words.uncommon_words],
    # ('track_lyrics_without_section_tags', 'artist_name'): [uncommon_words.uncommon_words],
    ('month', 'month'): [equal.equal],
    ('day_name', 'day_name'): [equal.equal],
    ('day', 'day'): [equal.equal],
    ('day_month', 'day_month'): [equal.equal],
    ('day_month_year', 'day_month_year'): [equal.equal],
    ('month_year', 'month_year'): [equal.equal],
    ('year', 'year'): [equal.equal],
    ('city_musicbrainz', 'city_musicbrainz'): [equal.equal],
    ('country_musicbrainz', 'country_musicbrainz'): [equal.equal],
    ('record_label_musicbrainz_id', 'record_label_musicbrainz_id'): [equal.equal],
    ('musical_genre_wikidata', 'musical_genre_wikidata'): [equal.equal],
    # ('album_uri_spotify', 'album_uri_spotify'): [equal.equal],
    # ('artist_uri_spotify', 'artist_uri_spotify'): [equal.equal],
    ('award_series', 'award_series'): [equal.equal],
    ('award_series_year', 'award_series_year'): [equal.equal],
    ('award_id_year', 'award_id_year'): [equal.equal],
    ('award_id', 'award_id'): [equal.equal],
    ('artist_type', 'artist_type'): [equal.equal],
    ('artist_self_releasing_records', 'artist_self_releasing_records'): [equal.equal],
}


def get_dict():
    return copy.deepcopy(_dict)


def resolve_compare_function(n1, n2, d=_dict):
    if (n1['type'], n2['type']) in d:

        v = d[(n1['type'], n2['type'])]
        if type(v) == dict:
            return resolve_compare_function(father(n1), father(n2), d=v)
        elif type(v) == list:
            return d[(n2['type'], n1['type'])]
        else:
            raise TypeError("Only nested dicts or lists are allowed")

    else:
        return []
