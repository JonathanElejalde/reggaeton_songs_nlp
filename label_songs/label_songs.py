def input_label(texts, target):
    """
    Takes a dict with inputs for each situation
    """
    value = input(texts[target])
    if target in ["sexual_content", "women_denigration"]:
        if value not in "012":
            raise ValueError("it is not a correct input")

    return value


# User itertuples() to iterate over each row in the dataframe
def label(df, texts):
    """
    Iterates over each row that has -1 in
    sexual_content and women_denigration, shows the lyrics
    and let add the labels for the respective columns
    """

    for i, row in df.iterrows():
        song_name, artist, lyrics, sexual_content, women_denigration, drugs = row
        if sexual_content == -1 or women_denigration == -1 or drugs == -1:
            print("######### START OF NEW SONG ####################################")
            print(lyrics)
            sexual_value = input_label(texts, "sexual_content")
            denigration_value = input_label(texts, "women_denigration")
            drugs_value = input_label(texts, "drugs")
            df.at[i, "sexual_content"] = int(sexual_value)
            df.at[i, "women_denigration"] = int(denigration_value)
            df.at[i, "drugs"] = int(drugs_value)

            print("\n" + str(song_name))
            # type y for updating otherwise continue

            update = input_label(texts, "update song_name")
            if update == "y":
                new_name = input("\nAdde song name: ")
                df.at[i, "song_name"] = new_name

            # save df
            df.to_csv("..\data\lyrics_labeled.csv", index=False)
        else:
            continue


if __name__ == "__main__":

    import sys
    import os
    import pandas as pd

    df = pd.read_csv("..\data\lyrics_labeled.csv")
    texts = {
        "sexual_content": "\nAdd 0 for non_sexual_content, 1 for explicit and 2 for implicit: ",
        "women_denigration": "\nAdd 0 for no denigration 1 for yes: ",
        "drugs": "\nAdd 0 for no drugs 1 for yes: ",
        "update song_name": "\nUpdate song name (y): ",
        "add song_name": "\nAdd song name: ",
    }

    try:
        label(df, texts)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
