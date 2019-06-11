__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
from empath import Empath

lexicon = Empath()
sns.set()

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']  # List of colors for the plot.

parser = argparse.ArgumentParser(description="""This script receives a folder containing '.csv' files created by 
                                                pushshift_comments.py and make emotion analysis of this files.""")

parser.add_argument("--src", dest="src", type=str, default="./data/reddit/cm/",
                    help="Source folder created by pushshift-comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./data/reddit/cm/analysis/",
                    help="Where to save the output files.")

parser.add_argument('-l', '--list', dest='emotion_list', default=['positive_emotion', 'love', 'friends', 'trust'],
                    nargs='+', help="List of emotions for the Empath analysis and graph plot."
                                    "Note: I recommend to pass an even number of elements for the list.")

args = parser.parse_args()


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
    for emotion in args.emotion_list:
        d[emotion] = []

    for comment in dataframe['Comment']:  # Gives an integer value for each emotion in each comment
        try:
            a = lexicon.analyze(comment)
            [d[emotion].append(a[emotion]/len(comment.split())) for emotion in args.emotion_list]
            # store the emotions value divided by the # words of each comment 
        except:
            [d[emotion].append(0) for emotion in args.emotion_list]  # if the analyze fail,
            # the comment is considered as a no emotion sentence.

    for emotion in args.emotion_list:
        dataframe[emotion] = d[emotion]

    print(f'columns added at {sub}')  # feedback while the process is running


def analyse_some_emotions(dataframe, sub):
    """
    Plot, for each subreddit, two rows of graphs, in the first, line plots with the mean of the emotions values by year
    and in the second, bar plots with the mean of emotions values by month.

    :param dataframe: Pandas DataFrame already process by the add_columns function.
    :param sub: String whit the name of the subreddit for the analysis.
    :return: GroupBy DataFrame for years, with an column of the means of the emotions values. Also saves the the
    plot in a image file on args.dst
    """
    series = []
    count = 0

    fig, axs = plt.subplots(nrows=2, ncols=(len(args.emotion_list)), figsize=(30, 20), sharey=True)
    fig.suptitle(sub, y=0.995, fontsize=45)

    for emotion in args.emotion_list:

        year_serie = dataframe.groupby('year')[emotion].mean()
        month_serie = dataframe.groupby('month')[emotion].mean()

        # Plot of emotions by year
        axs[0, count].plot(year_serie, ('-'), color=colors[count], linewidth=6)
        axs[0, count].set_title(f'{emotion}', fontsize=35)
        axs[0, count].set_xlabel("Year", fontsize=20)
        axs[0, count].set_ylabel("Emotion Mean", fontsize=20)

        # Plot of emotions by month
        axs[1, count].bar(list(month_serie.index), list(month_serie.values), color=colors[count])
        axs[1, count].set_title(f'{emotion}', fontsize=35)
        axs[1, count].set_xlabel("Month", fontsize=20)
        axs[1, count].set_ylabel("Emotion Mean", fontsize=20)
        month_list = list(month_serie.index[::12])
        axs[1, count].set_xticks(month_list)

        series.append(year_serie)
        count += 1

    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=30)
    plt.savefig(f'{args.dst}{sub}_good_emotions.png')
    plt.show()
    plt.close()

    emotions_by_year = pd.concat(series, axis=1, levels='emotion')
    emotions_by_year['year'] = list(emotions_by_year.index)
    return emotions_by_year


def plot_all_reddits_emotions(multi_emotions_by_year, subreddits):
    """
    Plot a big grid, with all the subreddits, and the evolution of all emotions by the years.

    :param multi_emotions_by_year: List of DataFrames returned by analyse_some_emotions()
    :param subreddits: List with all the subreddits names, founded in subreddits.csv
    :return: None and saves the plot in args.dst
    """
    c = 1  # Variable used to run throw all the elements of the lists
    collumns = int(len(multi_emotions_by_year) / 6) + 1  # This variable will be used in latter versions

    fig, axs = plt.subplots(nrows=6, ncols=5, figsize=(37, 30))
    fig.subplots_adjust(wspace=0.1, hspace=0.3)
    plt.rc('xtick', labelsize=40)
    plt.rc('ytick', labelsize=30)

    for row in range(6):
        for col in range(5):

            emotions_by_year = multi_emotions_by_year[c-1]
            emotions = emotions_by_year.melt('year', var_name='cols', value_name='Values')
            sns.barplot(x="year", y="Values", hue='cols', data=emotions,
                        palette='plasma', ax=axs[row, col])
            axs[row, col].set_title(str(subreddits[c-1])[5:-5], fontsize=35)

            if len(multi_emotions_by_year) == c:
                plt.savefig(f"{args.dst}grid_plot_good_emotions.png")
                plt.show()
                plt.close()
                return None

            c += 1


if __name__ == '__main__':
    print("Start")

    sdf = pd.read_csv('subreddits.csv')
    subreddits = sdf.values.tolist()

    multi_emotions_by_year = []

    for s in subreddits:
        sub = str(s)[5:-5]

        temp_df = pd.read_csv(f'{args.src}{sub}_comments.csv')
        add_columns(temp_df, sub)

        multi_emotions_by_year.append(analyse_some_emotions(temp_df, sub))

        if s == subreddits[0]:
            df = temp_df
        else:
            df = df.append(temp_df, ignore_index=True)

    multi_emotions_by_year.append(analyse_some_emotions(df, 'All Subs'))
    subreddits.append('.....All Subs....')

    plot_all_reddits_emotions(multi_emotions_by_year, subreddits)
