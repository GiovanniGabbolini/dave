from abydos.phonetic import NRL


def word_phonetics(word) -> 'phonetical_representation':
    phonetical_algorithm = NRL()
    return {'value': phonetical_algorithm.encode_alpha(word['value'])}
