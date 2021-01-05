import pandas as pd
import re

from spellchecker import SpellChecker


def remove_text_numbers(lyrics):
    """
    Takes the lyrics of a song and removes everything inside
    () or {} or [] and any number
    """
    pattern = r"[\(\[\{].*?[\)\]\}]"
    replace = ""
    new_lyrics = re.sub(pattern, replace, lyrics)

    # delete numbers
    number_pattern = r"\d+"
    new_lyrics = re.sub(number_pattern, replace, new_lyrics)

    return new_lyrics


def remove_special_chars(lyrics):
    """
    Takes the lyrics of a song and removes
    any special characters
    """

    replace = ""
    special_char_pattern = r"[^a-zA-Z \n\.]"
    new_lyrics = re.sub(special_char_pattern, replace, lyrics)

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
    # print(f"These are the duplicated indixes: {duplicate_index}")
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


def add_artists(df, spellchecker):
    """
    Takes a SpellChecker instance and loads the 
    artist's names to the dictionary
    """

    # add the artist names to the dictionary
    artists = df.artist.unique()
    artists_normalized = list()

    for artist in artists:
        artist = artist.lower().split()
        artists_normalized += artist

    artists = set(artists_normalized)

    spellchecker.word_frequency.load_words(artists)

    return spellchecker


def spell_checking(lyrics, spellchecker):
    """
    Takes the song lyrics and 
    correct misspelling words in the lyrics
    using an SpellChecker instance
    Args:
        lyrics: str
        spellchecker: SpellChecker(language='es') instance
    """

    # We are going to check spelling by line,
    # it will be easier to reconstruct the paragraphs
    new_lines = list()
    new_paragraphs = list()
    new_words = list()
    paragraphs = lyrics.split("\r\n\r\n")
    for paragraph in paragraphs:
        lines = paragraph.split("\r\n")

        for line in lines:
            words = [word for word in line.split()]

            # check each word
            for word in words:
                correction = spellchecker.correction(word)
                if word != correction:
                    print(word, ": ", correction)
                    word = correction

                new_words.append(word)

            # join the words in a line
            line = " ".join(new_words)
            new_lines.append(line)
            new_words = list()

        # join the lines in a paragraph
        paragraph = "\r\n".join(new_lines)
        new_paragraphs.append(paragraph)
        new_lines = list()

    # finally join the paragraphs into a full song
    new_lyrics = "\r\n\r\n".join(new_paragraphs)

    return new_lyrics


if __name__ == "__main__":
    pass
    # data_path = "..\data\lyrics_labeled.csv"

    # songs = pd.read_csv(data_path)

    # prueba = songs[:15]

    # prueba["lyrics"] = prueba.lyrics.apply(lambda x: remove_text(x))

    # l = prueba.iloc[4]
    # l = l.lyrics
    # l = remove_text_numbers(l)
    # l = avoid_repetition(l)
    # l = avoid_repetition(l, mode="lines")
    # l = remove_short_lines(l)

    # print(l)
    # song1 = "Bebé, Real Hasta La Muerte, baby\r\nAnuel\r\nW en conexión con Anuel (uah)\r\n\r\n[Anuel AA y Wisin]\r\nPensando en ti, pensando en mí (oah)\r\nYo perdí'o en tu silueta (Real Hasta La Muerte)\r\nTú encima 'e mí, yo encima 'e ti (oah)\r\nDevorándote completa (duro)\r\n\r\nPensando en ti, pensando en mí (uah, uah)\r\nTú mojándote en mi cama inquieta\r\nYo encima 'e ti, yo adentro 'e ti\r\nMientra' tú gritas y me aprieta' (señore', Doble U)\r\n\r\nDesde que te vi en el caserío supe que eso sería mío\r\nNos vimos en la disco y se formó un desafío\r\nNunca me olvido de ese día, los dos bien amanecío's\r\nTú estabas a fuego y yo seguía prendí'o\r\nEres atrevida, el amor de mi vida\r\nSon veinticinco en su corrillo y ella es la más temida\r\nVamos a vernos de nuevo y que nada lo impida\r\nTú sabes que hay muchas pero tú eres mi preferida\r\nTú me tiene' viviendo de los recuerdo'\r\nY ese totito yo te lo muerdo, uh, yeh\r\nYo quiero comerte, uah\r\nHasta la muerte, uah\r\n\r\n[Anuel AA]\r\nPensando en ti, pensando en mí\r\nYo perdí'o en tu silueta\r\nTú encima 'e mí, yo encima 'e ti (oah)\r\nDevorándote completa\r\n\r\nPensando en ti, pensando en mí (uah, uah)\r\nTú mojándote en mi cama inquieta\r\nYo encima 'e ti, yo adentro 'e ti\r\nMientra' tú gritas y me aprieta'\r\n\r\n[Wisin y Anuel AA]\r\nSigo preso en tu recuerdo\r\nTu olor aún siento en la habitación (W en conexión con Anuel)\r\nAquellas noches no consigo olvidar (yeh, eh)\r\nCierro mis ojos y te imagino aquí (Multimillo Records)\r\nMi cama pregunta por ti (Real Hasta La Muerte)\r\nQuisiera volverte a tocar (duro)\r\nRomeo y Julieta\r\nSin los condones y con la glopeta, 35, 000 en mi roleta\r\nBebecita, yo me vengo cuando tú grita\r\nY tú te viene cuando tu totito te palpita\r\n\r\nPensando en ti, pensando en mi\r\nYo adentro 'e tu cuerpo\r\nTú encima 'e mí, yo adentro e' ti\r\nTú ere' un oasis en el desierto\r\n\r\nTú me tienes viviendo de los recuerdos\r\nY ese cuellito yo te lo muerdo, uh, yeh\r\nYo quiero comerte, uah\r\nHasta la muerte, uah\r\n\r\n[Anuel AA]\r\nPensando en ti, pensando en mi\r\nYo perdí'o en tu silueta\r\nTú encima 'e mí, yo encima 'e ti\r\nDevorándote completa\r\n\r\nPensando en ti, pensando en mí\r\nTú mojándote en mi cama inquieta\r\nYo encima 'e ti, yo adentro 'e ti\r\nMientra' tú gritas y me aprieta'\r\n\r\n[Wisin y Anuel AA]\r\nBaby no disimules que tú te pones nerviosa cuando llegamo'\r\nCanciones como esta a muchos le dan alegría\r\nA otros le dan dolor de barriga\r\nJajajajaja\r\nChris Jeday, Gaby Music, Anuel, W\r\nSeñores; La Champions League\r\n(Real Hasta La Muerte, baby)\r\n¿Oí'te?\r\nLa Champions League\r\n(Uah)"

    # spell = SpellChecker(language="es")
    # spell = add_artists(songs, spell)
    # lyrics = spell_checking(song1, spell)

# print(lyrics)

