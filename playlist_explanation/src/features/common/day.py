from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def day(date)->'day':
    return {'value': date['value'].day}
