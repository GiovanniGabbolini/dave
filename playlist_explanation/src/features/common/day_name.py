from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def day_name(date) -> 'day_name':
    return {'value': date['value'].day_name()}
