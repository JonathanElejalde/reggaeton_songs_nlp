import pandas as pd
import langdetect

from langdetect import DetectorFactory

# Set the seed of the langdetect to reproducible results
detector_factory_seed = 10
DetectorFactory.seed = detector_factory_seed


def get_lang_probability(lang_prob):
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


def detect_songs_language(song_lyrics):
    """
    Takes the lyrics of a song and returns
    the languages that it has and the probabilities
    in a list of tuples
    Args:
        song_lyrics: str
    returns:
        lang_probs = list of tuples (lang, probability)
    """
    probs = langdetect.detect_langs(song_lyrics)
    lang_probs = list()
    for prob in probs:
        str_lang_prob = str(prob)
        lang_prob = get_lang_probability(str_lang_prob)
        lang_probs.append(lang_prob)

    return lang_probs


def delete_rows(df, rows):
    """
    It takes a dataframe and deletes the rows by index.
    Then it returns the resulting dataframe
    Args:
        df: pandas dataframe
        rows: list. list of indexes
    returns:
        df: pandas dataframe
    """
    df_len = len(df)
    print(f"The dataframe started with {df_len} rows")
    df = df.drop(index=rows)

    df_len = len(df)
    print(f"The dataframe ended with {df_len} rows")

    return df


def update_lyrics(lyrics):
    """
    Takes the lyrics of a song, splits it into
    paragraphs and detects the language of each
    paragraph. Finally joins the paragraphs that 
    are in spanish
    Args:
        lyrics: str
    returns:
        lyrics: str. The updated version of the song
            with just spanish
    """
    paragraphs = lyrics.split("\r\n\r\n")
    updated_lyrics = list()
    for paragraph in paragraphs:
        paragraph_lang = detect_songs_language(paragraph)

        # If the paragraph has more than one language skip it
        if len(paragraph_lang) > 1:
            continue

        lang, prob = paragraph_lang[0]

        if lang == "es":
            updated_lyrics.append(paragraph)
        else:
            print("This paragraph was deleted")
            print(paragraph)

    lyrics = "\r\n\r\n".join(updated_lyrics)

    return lyrics


if __name__ == "__main__":
    data_path = "..\data\lyrics_labeled.csv"
    lang_threshold = 0.80

    songs = pd.read_csv(data_path)

    prueba = songs[:100]

    def main(df, lang_threshold):
        # Store the indexes of the songs that are not in spanish or don't achieve the threshold
        delete_songs = list()

        # Store the indexes that are not complete spanish but achieve the threshold
        no_complete_spanish = list()

        count = 0
        no_spanish_count = 0
        for index, lyrics in df.lyrics.iteritems():
            lang_probs = detect_songs_language(lyrics)

            # If true it means the song has more than one language
            if len(lang_probs) > 1:

                # The first entry is the language with the highest probability
                lang, prob = lang_probs[0]

                if (lang == "es") and (prob > lang_threshold):
                    no_complete_spanish.append(index)
                    no_spanish_count += 1
                else:
                    count += 1
                    delete_songs.append(index)

            else:
                # when just one language check it is only spanish
                lang, prob = lang_probs[0]
                if lang != "es":
                    delete_songs.append(index)
                    count += 1

        # clean the lyrics that are not entirely in spanish
        for index in no_complete_spanish:
            lyrics = df.iloc[index].lyrics
            new_lyrics = update_lyrics(lyrics)

            # Change the dataframe in place
            df.at[index, "lyrics"] = new_lyrics

        songs_updated = delete_rows(df, delete_songs)
        songs_updated.to_csv("..\data\only_spanish_lyrics.csv", index=False)

    main(prueba, lang_threshold)

