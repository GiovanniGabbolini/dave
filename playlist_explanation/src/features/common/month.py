from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def month(date) -> 'month':
    return {'value': date['value'].month}
