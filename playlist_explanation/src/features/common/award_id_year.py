import re

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def award_id_year(award_wikidata) -> 'award_id_year':
    assert re.match(r"^\d{4}$", award_wikidata['value']['year'])
    return {'value':(award_wikidata['value']['award_id'], award_wikidata['value']['year'])}
