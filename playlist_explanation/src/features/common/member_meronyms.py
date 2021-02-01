from nltk.corpus import wordnet as wn


def member_meronyms(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).member_meronyms()]
