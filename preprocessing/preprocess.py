import pandas as pd

from spellchecker import SpellChecker
from detect_language import delete_no_spanish
from text_cleaning_spelling import (
    remove_text_numbers,
    avoid_repetition,
    remove_short_lines,
    add_artists,
    spell_checking,
)


def preprocess(df, lang_threshold):

    df_copy = df.copy()
    # Remove anything between (), {} or [] and any number
    df_copy["lyrics"] = df_copy.lyrics.apply(lambda x: remove_text_numbers(x))

    # Remove repeated paragraphs
    df_copy["lyrics"] = df_copy.lyrics.apply(lambda x: avoid_repetition(x))

    # Remove repeated lines
    df_copy["lyrics"] = df_copy.lyrics.apply(
        lambda x: avoid_repetition(x, mode="lines")
    )

    # Remove short lines than don't add significant meaning
    df_copy["lyrics"] = df_copy.lyrics.apply(lambda x: remove_short_lines(x))

    # Delete non-spanish lyrics and non-spanish paragraphs
    updated_df = delete_no_spanish(df_copy, lang_threshold)

    # Apply spelling correction
    spell = SpellChecker(language="es")
    spell = add_artists(updated_df, spell)
    updated_df["lyrics"] = updated_df.lyrics.apply(lambda x: spell_checking(x, spell))

    return updated_df


if __name__ == "__main__":
    data_path = "..\\data\\lyrics_labeled.csv"
    lang_threshold = 0.8
    songs = pd.read_csv(data_path)
    prueba = songs[:100]

    updated_df = preprocess(prueba, lang_threshold)
    updated_df.to_csv("..\\data\\updated_lyrics.csv", index=False)
