import pandas as pd
import pickle
from gensim.models.phrases import Phrases, Phraser

import time

import multiprocessing

from gensim.models import Word2Vec

from sqlitedict import SqliteDict

from datetime import datetime

pua_clean = SqliteDict("right_clean.sqlite", tablename="value", flag="r")
cores = multiprocessing.cpu_count() # Count the number of cores in a computer
parameters = dict(min_count=3,
                     window=2,
                     size=300,
                     sample=6e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20,
                     workers=cores-1)


def time_model_creation(model_sqlite, community):
    
    models = []
    years = []
    d = dict()
    sub = community
    year_sqlite = SqliteDict(f"{community}_years.sqlite", tablename="value", journal_mode="OFF")
    for id_c in model_sqlite:
        try:
            value = model_sqlite[id_c]
            dt_object = datetime.fromtimestamp(value["timestamp"]//1000)

            if dt_object.year not in years:
                print(dt_object.year)
                d[dt_object.year] = []
                years.append(dt_object.year)

            if value["text"] != None:
                d[dt_object.year].append(value["text"].split())
        except:
            print("ue")
            continue
                
    model_sqlite.close()
    print(years)
    
    for key, value in d.items():
        year_sqlite[key] = value
        
    year_sqlite.commit()
        
    for year in years:

        time_sent = year_sqlite[year]
        
        if len(time_sent) == 0:
            print(f"year {year} not found")
            continue
            
        time_phrases = Phrases(time_sent, min_count=3)
        time_bigram = Phraser(time_phrases)
        time_sentences = time_bigram[time_sent]
       
        with open(f"./../topic_model/data/{sub}_sentences_{year}.txt", "wb") as fp:  # Pickling
            pickle.dump(time_sentences, fp)
        print(f'{sub}_sentences_{year}.txt created')
        
        # Creating time Model
        Model = Word2Vec(**parameters)
        Model.build_vocab(time_sentences)
        Model.intersect_word2vec_format('GoogleNews-vectors-negative300.bin', lockf=1.0, binary=True)
        Model.train(time_sentences, total_examples=Model.corpus_count, epochs=30)
        
        Model.init_sims(replace=True)
        Model.wv.save(f"{sub}_wordvectors_{year}.kv")
        
        models.append(Model)
        
        print(f"Created {sub}_wordvectors_{year}.kv")
        
time_model_creation(pua_clean, "right")