import pandas as pd
import networkx as nx
import argparse
import itertools

parser = argparse.ArgumentParser(description="""This script receives a folder containing '.csv' files created by 
                                                pushshift_comments.py and make several analysis of this files """)

parser.add_argument("--src", dest="src", type=str, default="./data/reddit/cm/",
                    help="Source folder created by pushshift-comments  ")

parser.add_argument("--dst", dest="dst", type=str, default="./data/reddit/cm/analysis/",
                    help="Where to save the output files.")

parser.add_argument("--part", dest="part", type=bool, default=False,
                    help="Make a graph without the small reddits")

args = parser.parse_args()

def add_weigths(t, Gr):
    for i in range(len(t)):
        for j in range(i+1, len(t)):
            Gr.edges[t[i], t[j]]['weight'] += 1

sdf = pd.read_csv('./data/reddit/subreddits.csv')
subreddits = sdf.values.tolist()

for s in subreddits:
    sub = str(s)[5:-5]
    temp_df = pd.read_csv(f'{args.src}{sub}_comments.csv')
    temp_df = temp_df[temp_df.Author != '[deleted]']
    temp_au = pd.DataFrame(temp_df.groupby('Author')['Score'].sum())
    temp_au['sub'] = sub + ' '
    if s == subreddits[0]:
        df = temp_au
    else:
        df = df.append(temp_au)

    print(sub, 'collected')

relation = pd.DataFrame(df.groupby('Author')['sub'].sum())

G = nx.Graph()

for s in subreddits:
    sub = str(s)[5:-5]
    G.add_node(sub)

t = [str(s)[5:-5] for s in subreddits]
G.add_weighted_edges_from(itertools.product(t, t, [0]))

for Author in relation['sub']:
    sub = Author.split()
    if len(sub) > 1:
        add_weigths(sub, G)

nx.write_gexf(G, f"{args.dst}graph.gexf")

