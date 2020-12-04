import requests
from bs4 import BeautifulSoup


def save_file(artists, path):
    with open(path, "w") as f:
        for artist in artists:
            f.write(artist + "\n")


def load_file(path):
    with open(path, "r") as f:
        text = f.read()
        text = text.split("\n")

        return text


def read_pickle(filename):
    import pickle

    with open(filename, "rb") as fh:
        list_name = pickle.load(fh)

    return list_name


def save_pickle(filename, obj):
    import pickle

    with open(filename, "wb") as f:
        pickle.dump(obj, f)


def get_artists(url):

    result = requests.get(url)
    src = result.content

    soup = BeautifulSoup(src, "lxml")
    links = soup.find("ol", class_="top-list_art")

    artists = []
    for link in links.find_all("li"):
        link = link.find("a")
        url = link.attrs["href"]

        artists.append(url)

    return artists


def get_song_names(url):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    links = soup.find("ul", class_="cnt-list-songs -counter -top-songs js-song-list")

    songs = []
    for link in links.find_all("li"):
        link = link.find("a")
        song = link.attrs["href"]

        songs.append(song)

    return songs


def get_lyrics(url):
    result = requests.get(url)
    src = result.content

    soup = BeautifulSoup(src, "lxml")
    links = soup.find("div", class_="cnt-letra p402_premium")

    paragraphs = []
    try:
        for link in links.find_all("p"):
            # link.text returns all the text together
            # and we want the end of the line character as well
            # so we will use this approach instead.
            link = str(link)
            link = link.replace("<p>", "")
            link = link.replace("</p>", "")
            link = link.replace("<br/>", "\n")
            paragraphs.append(link)

        # Join all the paragraphs with a \n\n
        lyric = "\n\n".join(paragraphs)

        by = soup.find("div", class_="letra-info_comp")
        by = by.text

        return lyric, by

    except Exception as e:
        print(e)
        song = url.split("/")[-1]
        print(f"Error on song {song}")

        lyric = ""
        by = ""

        return lyric, by


if __name__ == "__main__":
    import os
    import time

    url_regguetton = "https://www.letras.com/mais-acessadas/reggaeton/"
    artists_path = "artists.txt"
    lyrics_path = "lyrics.pickle"
    base_url = "https://www.letras.com"
    end_url = "mais-tocadas.html"

    # Check if we already have the artist names
    if os.path.exists(artists_path):
        artists = load_file(artists_path)
    else:
        artists = get_artists(url_regguetton)
        save_file(artists, artists_path)

    # Check if we already started the dict with
    # the lyrics
    if os.path.exists(lyrics_path):
        lyrics = read_pickle(lyrics_path)
    else:
        lyrics = dict()
        save_pickle(lyrics_path, lyrics)

    for artist in artists[:200]:
        url_song = base_url + artist + end_url
        songs = get_song_names(url_song)

        if artist in lyrics.keys():
            print(f"{artist} already in lyrics")
            continue
        else:
            lyrics[artist] = {}

        for i, song in enumerate(songs, 1):
            url_lyrics = base_url + song
            text, by = get_lyrics(url_lyrics)

            # Save the lyrics
            lyrics[artist][song] = text
            lyrics[artist]["By"] = by

            print(f"Added {song} by {artist}")

            time.sleep(2)
        print(f"\n\nAdded {i} songs by the artist {artist}")
        save_pickle(lyrics_path, lyrics)
        time.sleep(5)
