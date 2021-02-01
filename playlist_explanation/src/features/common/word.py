from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def word(token_phrase) -> 'word':
    return {'value': token_phrase['value']}
