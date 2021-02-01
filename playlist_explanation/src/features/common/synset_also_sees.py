from nltk.corpus import wordnet as wn


def synset_also_sees(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).also_sees()]
