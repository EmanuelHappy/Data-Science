__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import pandas as pd
import argparse
from empath import Empath

lexicon = Empath()

parser = argparse.ArgumentParser(description="""This script receives a folder containing '.csv' files created by 
                                                pushshift_comments.py and make emotion analysis of this files.""")

parser.add_argument("--src", dest="src", type=str, default="./data/reddit/cm/",
                    help="Source folder created by pushshift-comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./data/reddit/cm/analysis/",
                    help="Where to save the output files.")

args = parser.parse_args()

emotion_list = ['sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']

def add_columns(dataframe, sub):
    """
    Add the needed columns fot the analysis.

    :param dataframe: Pandas DataFrame created by pushshift_comments.py for each subreddit.
    :param sub: String with the name of the Subreddit that will be analysed.
    :return: Nothing, but add columns in the current DataFrame.
    """
    date = dataframe['Publish Date']
    dataframe['num'] = 1  # number added for the GroupBy process
    dataframe['year'] = [item[:4] for item in date]
    dataframe['month'] = [item[:7] for item in date]
    dataframe['subreddit'] = sub

    d = {}  # dictionary where the emotions data will be stored
    for emotion in emotion_list:
        d[emotion] = []

    comm_serie = dataframe['Comment']
    for comment in comm_serie:  # Gives an integer value for each emotion in each comment
        try:
            a = lexicon.analyze(comment)
            [d[emotion].append(a[emotion] / len(comment.split())) for emotion in emotion_list]
            # store the emotions value divided by the number of words in the dataframe
        except:
            [d[emotion].append(-1.0) for emotion in emotion_list]  # if the analyze fail,
            # the emotion will be removed during the analysis

    for emotion in emotion_list:
        dataframe[emotion] = d[emotion]

    print(f'columns added at {sub}')  # feedback while the process is running

if __name__ == '__main__':
    print("Start")

    sdf = pd.read_csv('subreddits.csv')
    subreddits = sdf.values.tolist()

    for s in subreddits:
        sub = str(s)[5:-5]

        temp_df = pd.read_csv(f'{args.src}{sub}_comments.csv')
        temp_df = temp_df[temp_df.Comment != "[deleted]"]  # remove deleted comments
        add_columns(temp_df, sub)

        if s == subreddits[0]:
            df = temp_df
        else:
            df = df.append(temp_df, ignore_index=True)

    df.to_pickle(f"{args.dst}empath.csv")
    print(f"Created {args.dst}empath.csv")
