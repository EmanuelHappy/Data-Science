import re
import pandas as pd
from time import time
import spacy
import argparse

parser = argparse.ArgumentParser(description="""This script receives a folder containing '.csv' files created by 
                                                pushshift_comments.py and cleans the data for a future word embedding
                                                representation with of all the comments.""")

parser.add_argument("--src", dest="src", type=str, default="./../data/reddit/cm/",
                    help="Source folder created by pushshift-comments.")

parser.add_argument("--dst", dest="dst", type=str, default="",
                    help="Where to save the cleaned dataframe of the word embedding.")

parser.add_argument("--parser", dest="parser", type=bool, default=False,
                    help="If True, activate the parser processor of the words, it reduces speed, but improve the w2v")

args = parser.parse_args()

# Disabling Named Entity Recognition and Parser for speed
if not args.parser:
    nlp = spacy.load('en', disable=["ner", "parser"])
else:
    nlp = spacy.load('en')


def cleaning(doc):
    """
    :param doc: spacy Doc object processed by the pipeline
    :return: Text lemmatized and without stopwords
    """
    txt = [token.lemma_ for token in doc if not token.is_stop]

    # Since training with small document don't make great benefits, they are ignored.
    if len(txt) > 2:
        return ' '.join(txt)


if __name__ == "__main__":
    print("Start")

    # Loading data from the csv files.
    sdf = pd.read_csv('./../subreddits.csv')
    subreddits = sdf.values.tolist()

    for s in subreddits:
        sub = str(s)[5:-5]

        temp_df = pd.read_csv(f'{args.src}{sub}_comments.csv')

        if s == subreddits[0]:
            df = temp_df
        else:
            df = df.append(temp_df, ignore_index=True)

    # Small cleaning with re.
    brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in df['Comment'])
    print("Small cleaning completed")

    # Cleaning with spacy
    t = time()
    txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=32, n_threads=16)]
    print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))

    # Dataframe from the data
    df_clean = pd.DataFrame({'clean': txt})
    print(f"Number of comments = {df_clean.shape}")

    # Storing data to future analysis
    df_clean.to_pickle(f"{args.dst}df_clean.csv")
    print("df_clean.csv created")
