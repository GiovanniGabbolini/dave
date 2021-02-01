from nltk.corpus import wordnet as wn


def synset_similar_tos(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).similar_tos()]
