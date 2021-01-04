import pandas as pd
import langdetect

from langdetect import DetectorFactory

# Set the seed of the langdetect to reproducible results
detector_factory_seed = 10
DetectorFactory.seed = detector_factory_seed

# Delete entries where spanish is not the first language
# Where songs have multiple language delete paragraphs where spanish is not the principal


def get_data(path):
    """
    Reads a file and returns a pandas dataframe
    Args:
        path: str
    """

    df = pd.read_csv(path)

    return df


def get_lang_proba(lang_prob):
    """
    Takes a string with the format lang:probability and returns
    a tuple (lang, probability)
    Args:
        lang_prob: str
    """

    lang, probability = lang_prob.split(":")

    try:
        probability = float(probability)
    except Exception as e:
        print("Cound not convert probability to float")
        print(e)
    return (lang, probability)


def detect_songs_language(song):
    """
    Takes the lyrics of a song and returns
    the language with the highest probability and
    the probability
    Args:
        song: str
    returns:
        lang_prob = tuple (lang, probability)
    """
    probs = langdetect.detect_langs(song)

    # We assume that the first result is the highest
    str_lang_prob = str(probs[0])
    lang_prob = get_lang_proba(str_lang_prob)

    return lang_prob


if __name__ == "__main__":
    data_path = "..\data\lyrics_labeled.csv"

    songs = get_data(data_path)

    prueba = songs[:500]

    lyrics = prueba.lyrics[:20]

    count = 0
    for index, lyric in prueba.lyrics.iteritems():
        lang, prob = detect_songs_language(lyric)

        if lang != "es":
            print(lang, index)
            count += 1

        if (lang == "es") and (prob < 0.70):
            print(index)
            count += 1

print(f"Amount of songs to delete from the first 500 is {count}")
