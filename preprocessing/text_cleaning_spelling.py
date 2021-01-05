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
    print(f"These are the duplicated indixes: {duplicate_index}")
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


def remove_short_lines(lyrics):
    """
    Takes the lyrics of a song and removes
    lines with less than 3 words. Normally
    these lines don't have any meaningful meaning
    """
    paragraphs = lyrics.split("\r\n\r\n")
    new_paragraphs = list()
    new_lines = list()

    for paragraph in paragraphs:
        lines = paragraph.split("\r\n")
        for line in lines:
            tokens = line.split()

            if len(tokens) < 3:
                continue
            else:
                new_line = " ".join(tokens)
                new_lines.append(new_line)

        new_paragraph = "\r\n".join(new_lines)
        new_paragraphs.append(new_paragraph)
        new_lines = list()

    lyrics = "\r\n\r\n".join(new_paragraphs)

    return lyrics


# save a csv with clean text and spelling correction and without removing the repeated paragraphs and lines
# delete punctuation
# delete special characters
# delete numbers

# Run the cleaning again after spelling because there are some that still are the same lines but
# because of one single character are different

if __name__ == "__main__":
    data_path = "..\data\lyrics_labeled.csv"

    songs = pd.read_csv(data_path)

    prueba = songs[:10]

    # prueba["lyrics"] = prueba.lyrics.apply(lambda x: remove_text(x))

    l = prueba.iloc[2]
    l = l.lyrics
    l = remove_text(l)
    l = avoid_repetition(l)
    l = avoid_repetition(l, mode="lines")
    l = remove_short_lines(l)

    print(l)
    # final = avoid_repetition(l)
    # final = avoid_repetition(final, mode="lines")
