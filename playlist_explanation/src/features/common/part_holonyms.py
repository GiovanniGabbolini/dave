from nltk.corpus import wordnet as wn


def part_holonyms(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).part_holonyms()]
