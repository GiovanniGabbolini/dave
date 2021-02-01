from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def day_month(date) -> 'day_month':
    return {'value': (date['value'].day, date['value'].month)}
