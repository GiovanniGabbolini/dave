from src.text_processing.preprocess_word import stem


def word_stem(word) -> 'stem':
    return {'value': stem(word['value'])}
