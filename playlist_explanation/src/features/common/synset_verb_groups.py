from nltk.corpus import wordnet as wn


def synset_verb_groups(synset) -> 'synset':
    return [{'value': s.name()} for s in wn.synset(synset['value']).verb_groups()]
