from nltk.corpus import wordnet as wn

def antonyms(lemma) -> 'lemma':
    return [{'value': f"{l.synset().name()}.{l.name()}"} for l in wn.lemma(lemma['value']).antonyms()]
