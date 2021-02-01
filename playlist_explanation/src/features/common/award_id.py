from src.utils.decorator_annotations import annotations


@annotations({'entailed': True})
def award_id(award_wikidata) -> 'award_id':
    assert 'award_id' in award_wikidata['value'], "Bad formed award object"
    return {'value': award_wikidata['value']['award_id']}
