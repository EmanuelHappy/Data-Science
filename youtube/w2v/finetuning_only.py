import pandas as pd
import pickle
from gensim.models.phrases import Phrases, Phraser

import time

import multiprocessing

from gensim.models import Word2Vec

from sqlitedict import SqliteDict

from datetime import datetime
import numpy as np
import argparse
parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on perspective API scores of each youtube comment.""")



parser.add_argument("--year", dest="y", type=int, default="2018",
                    help="Comment where the analysis end.")
parser.add_argument("--epoch", dest="ep", type=int, default="1",
                    help="Comment where the analysis end.")
parser.add_argument("--loop", dest="loop", type=int, default="10",
                    help="Comment where the analysis end.")
parser.add_argument("--cat", dest="cat", type=str, default="Alt-lite",
                    help="Comment where the analysis end.")
parser.add_argument("--save", dest="save", type=bool, default=True,
                    help="Comment where the analysis end.")

args = parser.parse_args()



print("start")

name = args.cat
years=[args.y]

for year in years:
    #with open(f"{name}_clean_{year}.txt", "rb") as f:
    #    pua_clean = pickle.load(f)

    #pua_clean_csv = pd.read_pickle(f"{name}.sqlite_clean.csv")

    cores = multiprocessing.cpu_count() # Count the number of cores in a computer

    parameters = dict(min_count=50,
                         window=2,
                         size=300,
                         sample=6e-5, 
                         alpha=0.03, 
                         min_alpha=0.0007, 
                         negative=20,
                         workers=16)

    """
    sub_sent = []
    c = 0
    clean = np.array(pua_clean)
    print(clean.shape)
    for value in clean:
        if c%1000000==0:
            print(c)
        if(value != None):
            sub_sent.append(value.split())
        c+=1
    print("iter")
    sub_phrases = Phrases(sub_sent, min_count=3)
    print("phrases")
    sub_bigram = Phraser(sub_phrases)
    print("bigram")
    sub_sentences = sub_bigram[sub_sent]
    print("sentences")
    print("Start model")

    with open(f"{name}_sentences_{year}.txt", "wb") as fp:  # Pickling
        pickle.dump(sub_sentences, fp)
    print(f'{name}_sentences_{year}.txt created')"""
    
    with open(f"{name}_sentences_{year}.txt", "rb") as fp:
        sub_sentences = pickle.load(fp)
    print("Sub sentences loaded")
    
    if(args.ep==0):
        Model = Word2Vec(**parameters)
        Model.build_vocab(sub_sentences)
        print("build vocab")

        Model.intersect_word2vec_format('GoogleNews-vectors-negative300.bin', lockf=1.0, binary=True)
    
        print("intersect")
        Model.save(f"{name}_model_{year}.model")
    
    else:
        Model = Word2Vec.load(f"{name}_model_{year}.model")
        print(f"Previous loss={Model.get_latest_training_loss()/args.ep}")

        print("Model loaded")
        for i in range(args.loop):
            Model.train(sub_sentences, total_examples=Model.corpus_count, epochs=args.ep, compute_loss=True)
            print(f"train {i+1}, epochs={(i+1)*args.ep}, loss={Model.get_latest_training_loss()/args.ep}")
            Model.save(f"{name}_model_{year}.model")
            print(f"{name}_model_{year} saved")
    
    if(args.save):
        Model.init_sims(replace=True)
        print("pre-save")
        Model.wv.save(f"{name}_wordvectors_{year}.kv")
        print(f"{name}_wordvectors_{year}.kv saved")
    
