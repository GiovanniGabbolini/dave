from nltk.corpus import wordnet as wn


def member_holonyms(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).member_holonyms()]
