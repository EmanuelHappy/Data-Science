__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import string
from textblob import TextBlob
import argparse
from empath import Empath
lexicon = Empath()

parser = argparse.ArgumentParser(description="""This script receives a folder containing '.csv' files created by 
                                                pushshift_comments.py and make several analysis of this files """)

parser.add_argument("--src", dest="src", type=str, default="./data/reddit/cm/",
                    help="Source folder created by pushshift-comments  ")

parser.add_argument("--dst", dest="dst", type=str, default="./data/reddit/cm/analysis/",
                    help="Where to save the output files.")

args = parser.parse_args()


def add_columns(dataframe, sub, emotion_list):

    date = dataframe['Publish Date']
    dataframe['num'] = 1
    dataframe['year'] = [item[:4] for item in date]
    dataframe['month'] = [item[:7] for item in date]
    dataframe['subreddit'] = sub

    sentiment = []
    subjectivity = []

    """  for comment in dataframe['Comment']:
        try:
            sentiment.append(TextBlob(comment).sentiment[0])
            subjectivity.append(TextBlob(comment).sentiment[1])

        except:
            sentiment.append(0)
            subjectivity.append(0)

    dataframe['polarity'] = sentiment
    dataframe['subjectivity'] = subjectivity

    for emotion in emotion_list:
        emotions = []
        for comment in dataframe['Comment']:
            try:
                emotions.append(lexicon.analyze(str(comment))[emotion])
            except:
                emotions.append(0)

        dataframe[emotion] = emotions"""

    print(f'columns added at {sub}')


def process_comment_df(dataframe):
    hist = dict()
    for line in dataframe:
        process_line(str(line), hist)
    return hist


def process_line(line, hist):
    line = line.replace('-', ' ')
    for word in line.split():
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        hist[word] = hist.get(word, 0) + 1


def most_common_words(dataframe):
    Comment = dataframe['Comment']
    hist = process_comment_df(Comment)
    serie = pd.Series(list(hist.values()), index=list(hist.keys()))
    serie = serie.sort_values(ascending=False)
    num = np.arange(len(hist))
    order_of_words = pd.Series(num, index=serie.index)
    most_commom = pd.DataFrame({'appear': serie, 'rank': order_of_words})

    most_commom.to_csv(rf'{args.dst}most_common_words.csv', header=['appear', 'rank'])
    return most_commom


def reddit_activity(dataframe, sub):
    comments_per_month = pd.DataFrame(dataframe.groupby('month')['num'].sum())

    comments_per_month.pivot_table(index='month').plot()
    plt.legend(frameon=False)
    plt.title(f'{sub} activity')
    plt.savefig(f'{sub}_activity.png')
    plt.show()


def sentimental_analysis(dataframe, sub):
    sentiment = []
    subjectivity = []

    for comment in dataframe['Comment']:
        sentiment.append(TextBlob(str(comment)).sentiment[0])
        subjectivity.append(TextBlob(str(comment)).sentiment[1])

    dataframe['polarity'] = sentiment
    dataframe['subjectivity'] = subjectivity
    polarity_serie = dataframe.groupby('month')['polarity'].mean()
    subjectivity_serie = dataframe.groupby('month')['subjectivity'].mean()

    polarity_serie.plot()
    plt.legend(frameon=False)
    plt.title(f'{sub} polarity')
    plt.savefig(f'{sub}_polarity.png')
    plt.show()

    subjectivity_serie.plot()
    plt.legend(frameon=False)
    plt.title(f'{sub} subjectivity')
    plt.savefig(f'{sub}_subjectivity.png')
    plt.show()


def empath_rank(dataframe):

    analyze = lexicon.analyze(dataframe['Comment'][0])
    analyze_series = pd.Series(analyze)

    for comment in dataframe['Comment']:
        analyze_series += pd.Series(lexicon.analyze(str(comment)))

    sort = analyze_series.sort_values(ascending=False)
    empath_rank = pd.DataFrame(sort)
    empath_rank['rank'] = np.arange(len(sort))
    empath_rank.rename(columns={0: 'sum'}, inplace=True)

    empath_rank.to_csv(rf'{args.dst}empath_rank.csv', header=["appear", "rank"])
    return empath_rank

def analyse_some_emotions(dataframe, sub, emotion_list):

    series = []

    for emotion in emotion_list:
        serie = dataframe.groupby('year')[emotion].mean()

        plt.plot(serie, ('-'))
        plt.title(f'{sub} {emotion}')
        plt.savefig(f'{sub}_{emotion}_line.png')
        plt.show()

        a = sns.catplot(x="month", y=emotion, data=dataframe,
                        height=6, kind="bar", color="c", errwidth=0)
        plt.title(f'{sub} {emotion}')
        plt.show()
        a.savefig(f'{sub}_{emotion}_bar.png')

        series.append(serie)

    emotions_by_year = pd.concat(series, axis=1, levels='emotion')
    emotions_by_year['year'] = list(emotions_by_year.index)

    emotions = emotions_by_year.melt('year', var_name='cols', value_name='Values')
    g = sns.catplot(x="year", y="Values", hue='cols', kind='bar', data=emotions, height=9, palette='plasma')
    plt.title(f'{sub} emotions by year')
    plt.show()
    g.savefig(f"{sub}_emotions_by_year.png")

def comments_by_sub(dataframe):
    subs = dataframe.groupby('subreddit')['num'].sum()
    subs = subs.sort_values(ascending=False)

    subs.to_csv(rf'{args.dst}comments_by_sub.csv', header=['comments'])
    return subs

if __name__ == '__main__':
    sdf = pd.read_csv('subreddits.csv')
    subreddits = sdf.values.tolist()
    emotion_list = ['negative_emotion', 'hate', 'violence', 'death']

    for s in subreddits:
        sub = str(s)[5:-5]

        temp_df = pd.read_csv(f'{args.src}{sub}_comments.csv')
        add_columns(temp_df, sub, emotion_list)

        reddit_activity(temp_df, sub)

        #sentimental_analysis(temp_df, sub)

        #analyse_some_emotions(temp_df, sub, emotion_list)

        if s == subreddits[0]:
            df = temp_df
        else:
            df = df.append(temp_df, ignore_index=True)

    reddit_activity(df, 'all_subs')
    #sentimental_analysis(df, 'all_subs')
    #analyse_some_emotions(df, 'all_subs', emotion_list)
    #most_common_words(df)
    #comments_by_sub(df)
