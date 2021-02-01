from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def award_series(award_wikidata) -> 'award_series':
    if 'award_series' in award_wikidata['value']:
        return {'value': award_wikidata['value']['award_series']}
