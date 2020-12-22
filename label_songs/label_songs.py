import pandas as pd

df = pd.read_csv("..\data\lyrics_labeled.csv")

# iterate over each row
# read lyrics
# add values for content_sex column
# add values for women_denigration column
# add song_name if necessary and artits if needed

# User itertuples() to iterate over each row in the dataframe
def label(df):
    """
    Iterates over each row that has -1 in
    sexual_content and women_denigration, shows the lyrics
    and let add the labels for the respective columns
    """
    for i, row in df.iterrows():
        song_name, artist, lyrics, sexual_content, women_denigration = row
        if sexual_content == -1 and women_denigration == -1:
            print(lyrics)
            sexual_value = input(
                "\nAdd 0 for non_sexual_content, 1 for explicit and 2 for implicit: "
            )
            denigration_value = input("\nAdd 0 for no denigration 1 for yes: ")
            df.at[i, "sexual_content"] = int(sexual_value)
            df.at[i, "women_denigration"] = int(denigration_value)

            print("\n" + song_name)
            # type y for updating otherwise continue
            update = input("\nUpdate song name (y): ")
            if update == "y":
                new_name = input("\nAdde song name: ")
                df.at[i, "song_name"] = new_name

        break
    return df
    # if <condition>:
    #     ifor_val = something_else
    # df.at[i,'ifor'] = ifor_val


df_labeled = label(df)
df_labeled.to_csv("..\data\lyrics_labeled.csv")
