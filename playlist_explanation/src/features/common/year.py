from src.utils.decorator_annotations import annotations


@annotations({'entailed': True})
def year(date) -> 'year':
    return {'value': str(date['value'].year)}
