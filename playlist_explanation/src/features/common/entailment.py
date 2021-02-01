from nltk.corpus import wordnet as wn


def entailment(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).entailments()]
