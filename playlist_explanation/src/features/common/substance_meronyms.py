from nltk.corpus import wordnet as wn


def substance_meronyms(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).substance_meronyms()]
