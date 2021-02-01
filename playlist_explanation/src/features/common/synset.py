from nltk.corpus import wordnet as wn


def synset(word) -> 'synset':
    synsets = wn.synsets(word['value'])
    # Keep just the first first sense, favouring stronger associations
    if len(synsets) > 0:
        return {'value': synsets[0].name()}
