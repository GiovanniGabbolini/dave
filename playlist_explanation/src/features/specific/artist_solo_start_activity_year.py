"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_cached_feature import cached_feature
from src.sparql.query_sparql_wikidata import query_sparql
import re
import logging


@cached_feature
@timing_feature
def artist_solo_start_activity_year(artist_wikidata_id, artist_type) -> 'year':
    """Extracts the year a solo artist has started his musical career

    Arguments:
        artist_wikidata_id {str} -- 
        artist_solo {str} -- 

    Returns:
        str -- Year, formatted as a string with 4 digits. Eg. 1994
    """
    if artist_wikidata_id is not None and artist_type['value'] == 'Person':
        query = "select ?y where {" + \
            artist_wikidata_id['value'] + " wdt:P2031 ?y .}"
        results = query_sparql(query)
        if len(results) > 0:
            if len(results) == 1:
                date = results[0]['y']['value']

                # Check if satisfies the pattern
                if re.match(r"^\d{4}-\d{2}-\d{2}T00:00:00Z$", date):
                    year = date.split('-')[0]
                    return {'value': year}
                else:
                    logging.getLogger('root.features').warning(
                        f"Date {date} does not match pattern")
            else:
                logging.getLogger('root.features').warning(
                    f"Found more than one value for work period (start) for entity {artist_wikidata_id['value']}, skipping")

        else:
            logging.getLogger('root.features').warning(
                f"No attribute work period (start) associated with entity {artist_wikidata_id['value']}")


if __name__ == "__main__":
    array_feature(artist_solo_start_activity_year, mp=True)
