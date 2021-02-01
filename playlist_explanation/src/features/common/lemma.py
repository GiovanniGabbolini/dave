from nltk.corpus import wordnet as wn


def lemma(word) -> 'lemma':
    lemmas = wn.lemmas(word['value'])
    return [{'value': f"{l.synset().name()}.{l.name()}"} for l in lemmas]
