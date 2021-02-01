from src.data.genres_musicbrainz_to_wikidata import genres_musicbrainz_to_wikidata
from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def musical_genre_musicbrainz_to_wikidata(musical_genre_musicbrainz_id) -> 'musical_genre_wikidata':
    genre_wikidata = genres_musicbrainz_to_wikidata(musical_genre_musicbrainz_id['value'])
    if genre_wikidata is not None:
        return {'value': genre_wikidata}
