from src.utils.decorator_annotations import annotations


@annotations({'entailed': True})
def day_month_year(date) -> 'day_month_year':
    return {'value': (date['value'].day, date['value'].month, date['value'].year)}
