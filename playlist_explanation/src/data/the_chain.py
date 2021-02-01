import pandas as pd
import requests
import os
from src.data import data
from bs4 import BeautifulSoup
import pandas as pd
from src.knowledge_graph.io import save_sub_graphs


def get_last_element_the_chain():
    link = "https://www.thechain.uk/"

    req = requests.get(link)
    if not req.ok:
        if req.reason == 'Not Found':
            raise Exception

    soup = BeautifulSoup(req.text, "lxml")
    titles = soup.find_all("h1", {'class': 'entry-title'})
    t = titles[0]

    section_title = t.text
    if len(section_title.split('.')) == 2:
        title = section_title.split('.')[1]
    elif len(section_title.split('.')) > 2:
        title = '.'.join(section_title.split('.')[1:])
        print(
            f"Splitting {section_title} with '.' led to more than a number of substrings different from 2. Considering {title} as title")
    else:
        raise Exception(
            "Splitting section title with . led to a number of substrings lower than 2! Error!!!")

    if '–' in title:
        splitting_char = '–'
    elif '-' in title:
        splitting_char = '-'
    else:
        raise Exception(
            "No - neither – was found in song title! Error!!!!")

    if len(title.split(splitting_char)) > 2:
        artist_name = title.split(splitting_char)[0].strip()
        song_name = splitting_char.join(
            title.split(splitting_char)[1:]).strip()
        print(
            f"splitting {title} with {splitting_char} led to a number of substrings different from 2! \
            Considering artist_name: {artist_name} and song_name: {song_name}")
    elif len(title.split(splitting_char)) == 2:
        artist_name = title.split(splitting_char)[0].strip()
        song_name = title.split(splitting_char)[1].strip()

    return {'artist_name': artist_name, 'track_name': song_name}


def scrape_the_chain():
    segues = []
    track_names = []
    artist_names = []

    page_count = 0
    while True:
        print(page_count)
        if page_count == 0:
            link = "https://www.thechain.uk/"
        else:
            link = f"https://www.thechain.uk/page/{page_count}"

        req = requests.get(link)
        if not req.ok:
            if req.reason == 'Not Found':
                break

        soup = BeautifulSoup(req.text, "lxml")
        titles = soup.find_all("h1", {'class': 'entry-title'})
        contents = soup.find_all("div", {'class': 'entry-content'})
        for t in titles:
            section_title = t.text
            if len(section_title.split('.')) == 2:
                title = section_title.split('.')[1]
            elif len(section_title.split('.')) > 2:
                title = '.'.join(section_title.split('.')[1:])
                print(
                    f"Splitting {section_title} with '.' led to more than a number of substrings different from 2. Considering {title} as title")
            else:
                raise Exception(
                    "Splitting section title with . led to a number of substrings lower than 2! Error!!!")

            if '–' in title:
                splitting_char = '–'
            elif '-' in title:
                splitting_char = '-'
            else:
                raise Exception(
                    "No - neither – was found in song title! Error!!!!")

            if len(title.split(splitting_char)) > 2:
                artist_name = title.split(splitting_char)[0].strip()
                song_name = splitting_char.join(
                    title.split(splitting_char)[1:]).strip()
                print(
                    f"splitting {title} with {splitting_char} led to a number of substrings different from 2! \
                    Considering artist_name: {artist_name} and song_name: {song_name}")
            elif len(title.split(splitting_char)) == 2:
                artist_name = title.split(splitting_char)[0].strip()
                song_name = title.split(splitting_char)[1].strip()

            artist_names.insert(0, artist_name)
            track_names.insert(0, song_name)

        for c in contents:
            segues.insert(0, c.next.text)

        page_count += 1

    df = pd.DataFrame({'track_name': track_names,
                       'artist_name': artist_names, 'links': segues})
    df.to_csv(os.path.join(data.raw_dataset_path, "the_chain.csv"))


def save_graph_the_chain():
    the_chain = pd.read_csv(f"{data.raw_dataset_path}/the_chain.csv")

    l = []
    for track_name, artist_name in zip(the_chain.track_name, the_chain.artist_name):
        d = {
            'track_name': track_name,
            'artist_name': artist_name,
        }
        l.append(d)

    save_sub_graphs(l, folder_name="sub_graphs_the_chain")


if __name__ == "__main__":
    save_graph_the_chain()
