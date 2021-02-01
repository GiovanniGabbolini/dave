from nltk.corpus import wordnet as wn


def synset_attributes(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).attributes()]
