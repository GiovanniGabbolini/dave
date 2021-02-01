
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import sys
from src.data.data import preprocessed_dataset_path


def build_genres_dictionary():
    """Build a dictionary having:
    - As keys: name of genres tags in musicbrainz (https://musicbrainz.org/genres)
    - As values: ids of genres in musicbrainz
    """
    sys.setrecursionlimit(10000)
    genres_names = ['acid house',
                    'acid jazz',
                    'acid techno',
                    'acoustic blues',
                    'acoustic rock',
                    'afrobeat',
                    'alternative country',
                    'alternative dance',
                    'alternative folk',
                    'alternative hip hop',
                    'alternative metal',
                    'alternative pop',
                    'alternative punk',
                    'alternative rock',
                    'ambient',
                    'ambient house',
                    'ambient techno',
                    'americana',
                    'anarcho-punk',
                    'aor',
                    'arena rock',
                    'art rock',
                    'atmospheric black metal',
                    'audiobook',
                    'avant-garde',
                    'avant-garde jazz',
                    'avant-garde metal',
                    'avant-garde pop',
                    'bachata',
                    'ballad',
                    'barbershop',
                    'baroque',
                    'bebop',
                    'bhangra',
                    'big band',
                    'big beat',
                    'black metal',
                    'blackened death metal',
                    'blackgaze',
                    'blue-eyed soul',
                    'bluegrass',
                    'blues',
                    'blues rock',
                    'bolero',
                    'bolero son',
                    'boom bap',
                    'bossa nova',
                    'breakbeat',
                    'breakcore',
                    'breaks',
                    'britpop',
                    'broken beat',
                    'brutal death metal',
                    'bubblegum pop',
                    'cajun',
                    'calypso',
                    'canterbury scene',
                    'cantopop',
                    'celtic',
                    'celtic punk',
                    'chamber pop',
                    'champeta',
                    'chanson',
                    'chicago blues',
                    'chillout',
                    'chiptune',
                    'christian rock',
                    'christmas music',
                    'city pop',
                    'classic blues',
                    'classic country',
                    'classic jazz',
                    'classic rock',
                    'classical',
                    'club',
                    'comedy',
                    'conscious hip hop',
                    'contemporary christian',
                    'contemporary classical',
                    'contemporary folk',
                    'contemporary gospel',
                    'contemporary jazz',
                    'contemporary r&b',
                    'contra',
                    'cool jazz',
                    'country',
                    'country blues',
                    'country folk',
                    'country pop',
                    'country rock',
                    'crossover prog',
                    'crust punk',
                    'cumbia',
                    'd-beat',
                    'dance',
                    'dance-pop',
                    'dance-punk',
                    'dancehall',
                    'dark ambient',
                    'dark electro',
                    'dark folk',
                    'dark wave',
                    'death metal',
                    'death-doom metal',
                    'deathcore',
                    'deathgrind',
                    'deathrock',
                    'deep house',
                    'delta blues',
                    'desert rock',
                    'digital hardcore',
                    'disco',
                    'doo-wop',
                    'doom metal',
                    'downtempo',
                    'drill',
                    'drone',
                    'drum and bass',
                    'dub',
                    'dub techno',
                    'dubstep',
                    'dungeon synth',
                    'east coast hip hop',
                    'ebm',
                    'electric blues',
                    'electro',
                    'electro house',
                    'electro swing',
                    'electro-funk',
                    'electro-industrial',
                    'electroclash',
                    'electronic',
                    'electronic rock',
                    'electronica',
                    'electronicore',
                    'electropop',
                    'electropunk',
                    'emo',
                    'emocore',
                    'enka',
                    'ethereal',
                    'euro house',
                    'eurodance',
                    'europop',
                    'experimental',
                    'experimental rock',
                    'fado',
                    'filk',
                    'flamenco',
                    'folk',
                    'folk metal',
                    'folk pop',
                    'folk punk',
                    'folk rock',
                    'freak folk',
                    'free improvisation',
                    'free jazz',
                    'funk',
                    'funk carioca',
                    'funk metal',
                    'funk rock',
                    'funk soul',
                    'funky house',
                    'fusion',
                    'future jazz',
                    'futurepop',
                    'g-funk',
                    'gabber',
                    'gangsta rap',
                    'garage',
                    'garage house',
                    'garage punk',
                    'garage rock',
                    'glam',
                    'glam metal',
                    'glam rock',
                    'glitch',
                    'goa trance',
                    'goregrind',
                    'gospel',
                    'gothic',
                    'gothic metal',
                    'gothic rock',
                    'grebo',
                    'grime',
                    'grindcore',
                    'groove metal',
                    'grunge',
                    'guaracha',
                    'happy hardcore',
                    'hard bop',
                    'hard house',
                    'hard rock',
                    'hard trance',
                    'hardcore punk',
                    'hardcore techno',
                    'hardstyle',
                    'heavy metal',
                    'hip hop',
                    'honky tonk',
                    'horror punk',
                    'horrorcore',
                    'house',
                    'idm',
                    'illbient',
                    'indie',
                    'indie folk',
                    'indie pop',
                    'indie rock',
                    'indietronica',
                    'indorock',
                    'industrial',
                    'industrial metal',
                    'industrial rock',
                    'instrumental',
                    'instrumental jazz',
                    'instrumental rock',
                    'irish folk',
                    'italo-disco',
                    'j-pop',
                    'j-rock',
                    'jazz',
                    'jazz blues',
                    'jazz fusion',
                    'jazz rap',
                    'jazz rock',
                    'jazz-funk',
                    'jungle',
                    'k-pop',
                    'kayōkyoku',
                    'kizomba',
                    'klezmer',
                    'krautrock',
                    'latin',
                    'latin jazz',
                    'latin pop',
                    'latin rock',
                    'leftfield',
                    'line dance',
                    'lo-fi',
                    'lounge',
                    'lovers rock',
                    'madchester',
                    'mainstream rock',
                    'mambo',
                    'mandopop',
                    'martial industrial',
                    'math rock',
                    'mathcore',
                    'medieval',
                    'melodic black metal',
                    'melodic death metal',
                    'melodic metalcore',
                    'melodic rock',
                    'melodic trance',
                    'mento',
                    'merengue',
                    'metal',
                    'metalcore',
                    'microhouse',
                    'milonga',
                    "min'yō",
                    'mincecore',
                    'minimal',
                    'modern blues',
                    'modern classical',
                    'modern country',
                    'motown',
                    'mpb',
                    'musical',
                    'neo soul',
                    'neo-progressive rock',
                    'neo-rockabilly',
                    'neofolk',
                    'nerdcore',
                    'new age',
                    'new jack swing',
                    'new romantic',
                    'new wave',
                    'no wave',
                    'noise',
                    'noise pop',
                    'noisecore',
                    'non-music',
                    'norteño',
                    'northern soul',
                    'nu jazz',
                    'nu metal',
                    'occult rock',
                    'oi',
                    'old school death metal',
                    'old-time',
                    'opera',
                    'orchestral',
                    'outlaw country',
                    'p-funk',
                    'pachanga',
                    'pop',
                    'pop metal',
                    'pop punk',
                    'pop rap',
                    'pop rock',
                    'pop soul',
                    'pornogrind',
                    'post-bop',
                    'post-classical',
                    'post-grunge',
                    'post-hardcore',
                    'post-metal',
                    'post-punk',
                    'post-rock',
                    'power electronics',
                    'power metal',
                    'power pop',
                    'powerviolence',
                    'production music',
                    'progressive',
                    'progressive folk',
                    'progressive house',
                    'progressive metal',
                    'progressive rock',
                    'progressive trance',
                    'psy-trance',
                    'psychedelic',
                    'psychedelic folk',
                    'psychedelic pop',
                    'psychedelic rock',
                    'psychobilly',
                    'psytrance',
                    'punk',
                    'punk rock',
                    'queercore',
                    'r&b',
                    'ragga',
                    'ragga hip-hop',
                    'ragga jungle',
                    'ragtime',
                    'raï',
                    'ranchera',
                    'rap rock',
                    'rapcore',
                    'rave',
                    'reggae',
                    'reggaeton',
                    'rhythmic noise',
                    'rock',
                    'rock and roll',
                    'rockabilly',
                    'rocksteady',
                    'roots reggae',
                    'rumba',
                    'salsa',
                    'samba',
                    'schlager',
                    'screamo',
                    'shibuya-kei',
                    'shoegaze',
                    'singer-songwriter',
                    'ska',
                    'ska punk',
                    'skacore',
                    'slow waltz',
                    'sludge metal',
                    'smooth jazz',
                    'smooth soul',
                    'soca',
                    'soft rock',
                    'son cubano',
                    'son montuno',
                    'soul',
                    'soul jazz',
                    'southern rock',
                    'southern soul',
                    'space rock',
                    'speed garage',
                    'speed metal',
                    'spoken word',
                    'stoner metal',
                    'stoner rock',
                    'street punk',
                    'surf rock',
                    'swing',
                    'symphonic black metal',
                    'symphonic metal',
                    'symphonic prog',
                    'symphonic rock',
                    'symphony',
                    'synth-pop',
                    'synthwave',
                    'tango',
                    'tech house',
                    'technical death metal',
                    'techno',
                    'teen pop',
                    'thrash metal',
                    'thrashcore',
                    'timba',
                    'traditional country',
                    'trance',
                    'trap',
                    'trap edm',
                    'tribal house',
                    'trip hop',
                    'turntablism',
                    'uk drill',
                    'uk garage',
                    'underground hip hop',
                    'vallenato',
                    'vaporwave',
                    'viking metal',
                    'visual kei',
                    'vocal house',
                    'vocal jazz',
                    'vocal trance',
                    'west coast hip hop',
                    'west coast swing',
                    'yé-yé',
                    'zamrock',
                    'zydeco', ]
    req = requests.get("https://musicbrainz.org/genres")
    soup = BeautifulSoup(req.text, "html.parser")
    titles = soup.find_all("a")
    genres = {}
    for tag in titles:
        if re.match(r'^<a href=\"/genre/[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}\"><bdi>(\S| )+</bdi></a>$', str(tag)):
            genre_id = str(tag.attrs['href']).split('/')[-1]
            genre_name = tag.bdi.string
            genres[genre_name] = genre_id

    genres_keys = list(genres.keys())

    np.save(f'{preprocessed_dataset_path}/musicbrainz_genres_dictionary', genres)


def genres_musicbrainz(key):
    """Given a tag name in musicbrainz, returns the genre id in musicbrainz, in case the tag is associated to a musical genre

    Arguments:
        key {str} -- 

    Raises:
        FileNotFoundError: In case the genres dictionary is missing
        KeyError: In case the tag value does not resolve to a genre

    Returns:
        str -- musicbrainz id of the genre
    """
    try:
        d = np.load(f'{preprocessed_dataset_path}/musicbrainz_genres_dictionary.npy',
                    allow_pickle=True).item()
    except FileNotFoundError:
        raise FileNotFoundError(
            "Musicbrainz genres dictionary is missing. Create using function build_genres_dictionary in genres_musicbrainz.py")

    try:
        musicbrainz_genre_id = d[key]
    except KeyError:
        raise KeyError(
            f"Genre {key} not found in musicbrainz genre dictionary.")

    return musicbrainz_genre_id


if __name__ == "__main__":
    build_genres_dictionary()
