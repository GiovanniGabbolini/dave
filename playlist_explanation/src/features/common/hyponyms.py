from nltk.corpus import wordnet as wn


def hyponyms(synset) -> 'synset':
    return [{'value': l.name()} for l in wn.synset(synset['value']).hyponyms()]
