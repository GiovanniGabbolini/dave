from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def month_year(date)-> 'month_year':
    return {'value': (date['value'].month, date['value'].year)}
