import pandas as pd
import re


def remove_text(lyrics):
    """
    Takes the lyrics of a song and removes everything inside
    () or {} or []
    """
    pattern = r"[\(\[\{].*?[\)\]\}]"
    replace = ""
    new_lyrics = re.sub(pattern, replace, lyrics)

    return new_lyrics


def avoid_repetition(lyrics, mode="paragraphs"):
    """
    Takes the lyrics of a song and removes
    paragraphs or lines that appear more than once.
    Args:
        lyrics: str
        mode: str. It can be paragraphs or lines
    """
    if mode == "paragraphs":
        splits = lyrics.split("\r\n\r\n")
    elif mode == "lines":
        splits = lyrics.split("\r\n")

    new_lyrics = list()
    duplicate_index = list()

    empty_lines = 0
    for i, split in enumerate(splits):
        split = split.strip()

        # avoid looping through duplicates
        if i in duplicate_index:
            continue

        # avoid empty lines
        if len(split) <= 1:
            empty_lines += 1
            continue

        for j, split2 in enumerate(splits):
            split2 = split2.strip()

            if i == j:
                continue

            if split == split2:
                duplicate_index.append(j)
    # print(duplicate_index)
    # if mode == "lines":
    #     print(f"Amount of empty lines {empty_lines}")

    for i, split in enumerate(splits):
        if i not in duplicate_index:
            new_lyrics.append(split)

    if mode == "paragraphs":
        lyrics = "\r\n\r\n".join(new_lyrics)
    elif mode == "lines":
        lyrics = "\r\n".join(new_lyrics)

    return lyrics


def remove_repeated_lines(lyrics):
    """
    Takes the lyrics of a song without repeated paragraphs
    and removes any line that appears more than once
    """


# save a csv with clean text and spelling correction and without removing the repeated paragraphs and lines
# Delete words and phrases between () {} []
# Delete repeated paragraphs
# delete repeated lines
# delete short lines - meaning lines with less than 3 words normally don't bring meaningful meaning
# delete punctuation
# delete special characters
# delete numbers

if __name__ == "__main__":
    data_path = "..\data\lyrics_labeled.csv"

    songs = pd.read_csv(data_path)

    prueba = songs[:10]

    # prueba["lyrics"] = prueba.lyrics.apply(lambda x: remove_text(x))

    l = prueba.iloc[0]
    l = l.lyrics
    l = avoid_repetition(l)
    l = avoid_repetition(l, mode="lines")
    print(l)

