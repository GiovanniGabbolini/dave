import re

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def award_year(award_wikidata) -> 'year':
    assert 'year' in award_wikidata['value'], "Bad formed award object"
    assert re.match(r"^\d{4}$", award_wikidata['value']['year'])
    return {'value': award_wikidata['value']['year']}
