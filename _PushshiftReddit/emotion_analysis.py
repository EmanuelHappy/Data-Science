__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
from empath import Empath
lexicon = Empath()
sns.set()

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

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

    d = {}
    for emotion in emotion_list:
        d[emotion] = []

    for comment in dataframe['Comment']:
        try:
            a = lexicon.analyze(str(comment))
            [d[emotion].append(a[emotion]) for emotion in emotion_list]
        except:
            [d[emotion].append(0) for emotion in emotion_list]

    for emotion in emotion_list:
        dataframe[emotion] = d[emotion]

    print(f'columns added at {sub}')


def analyse_some_emotions(dataframe, sub, emotion_list):

    series = []
    count = 0

    fig, axs = plt.subplots(nrows=2, ncols=(len(emotion_list)), figsize=(30, 20))
    fig.subplots_adjust(wspace=0.3, hspace=0.3)
    for emotion in emotion_list:
        year_serie = dataframe.groupby('year')[emotion].mean()
        month_serie = dataframe.groupby('month')[emotion].mean()

        axs[0, count].plot(year_serie, ('-'), color=colors[count], linewidth=6)
        axs[0, count].set_title(f'{sub} {emotion}', fontsize=23)
        axs[0, count].set_xlabel("Year", fontsize=20)
        axs[0, count].set_ylabel("Emotion Mean", fontsize=20)

        axs[1, count].bar(list(month_serie.index), list(month_serie.values), color=colors[count])
        axs[1, count].set_title(f'{sub} {emotion}', fontsize=23)
        axs[1, count].set_xlabel("Month", fontsize=20)
        axs[1, count].set_ylabel("Emotion Mean", fontsize=20)
        month_list = list(month_serie.index[::10])
        axs[1, count].set_xticks(month_list)

        series.append(year_serie)
        count += 1

    plt.savefig(f'{sub}_bad_emotions.png')
    plt.show()
    plt.close()


    emotions_by_year = pd.concat(series, axis=1, levels='emotion')
    emotions_by_year['year'] = list(emotions_by_year.index)
    return emotions_by_year


def plot_all_reddits_emotions(multi_emotions_by_year, subreddits):
    c = 1
    collumns = int(len(multi_emotions_by_year) / 1) + 1
    fig, axs = plt.subplots(nrows=6, ncols=collumns, figsize=(37, 30))
    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    for row in range(1):
        for col in range(collumns):

            emotions_by_year = multi_emotions_by_year[collumns*row + col]
            emotions = emotions_by_year.melt('year', var_name='cols', value_name='Values')
            sns.barplot(x="year", y="Values", hue='cols', data=emotions,
                        palette='plasma', ax=axs[row, col])

            if len(multi_emotions_by_year) == c:
                plt.savefig("all_subs_bad_emotions.png")
                plt.show()
                plt.close()
                return None

            c+=1
    #g.savefig(f"{args.dst}{sub}_emotions_by_year.png")'''


if __name__ == '__main__':
    print("Start")
    sdf = pd.read_csv('subreddits.csv')
    subreddits = sdf.values.tolist()
    emotion_list = ['negative_emotion', 'hate', 'violence', 'death']
    multi_emotions_by_year = []

    for s in subreddits[1:4]:
        sub = str(s)[5:-5]
        print(sub)

        temp_df = pd.read_csv(f'{args.src}{sub}_comments.csv')
        add_columns(temp_df, sub, emotion_list)

        multi_emotions_by_year.append(analyse_some_emotions(temp_df, sub, emotion_list))

        if s == subreddits[1]:
            df = temp_df
        else:
            df = df.append(temp_df, ignore_index=True)

    multi_emotions_by_year.append(analyse_some_emotions(df, 'all_subs', emotion_list))
    print(len(multi_emotions_by_year))
    plot_all_reddits_emotions(multi_emotions_by_year, subreddits)
