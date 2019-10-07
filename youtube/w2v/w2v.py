import re
import pandas as pd
import spacy
import numpy as np
from multiprocessing import Pool
from sqlitedict import SqliteDict
from time import time
from datetime import datetime
nlp = spacy.load('en', disable=["ner", "parser"])
import pickle
print("Start")

def cleaning(doc):
    """
    :param doc: spacy Doc object processed by the pipeline
    :return: Text lemmatized and without stopwords
    """
    try:
        txt = [token.lemma_ for token in doc if not token.is_stop]

        # Since training with small document don't make great benefits, they are ignored.
        if len(txt) > 2:
            return ' '.join(txt)
    except:
        print(doc)
        return ' '
categories = ["Alt-right"]
years = [2012, 2015, 2017, 2018, 2019]
for category in categories:
    print(f"Category = {category}")

    #pua = SqliteDict(f"./../Sqlite/split_texts/{category}.sqlite", tablename="value", flag="r")

    #	pua_clean = SqliteDict(f"{category}_clean.sqlite", tablename="value", journal_mode="OFF")
    """
    pre_cleaning1 = []
    pre_cleaning2 = []
    pre_cleaning3 = []
    pre_cleaning4 = []
    pre_cleaning5 = []
    c=0
    for value in pua.values():
        try:
            y = datetime.fromtimestamp(value["timestamp"]//1000).year
            if y<=2012:
                pre_cleaning1.append(re.sub("[^A-Za-z]+", ' ', str(value["text"]).lower()))
            elif y<=2015:
                pre_cleaning2.append(re.sub("[^A-Za-z]+", ' ', str(value["text"]).lower()))
            elif y<=2017:
                pre_cleaning3.append(re.sub("[^A-Za-z]+", ' ', str(value["text"]).lower()))
            elif y<=2018:
                pre_cleaning4.append(re.sub("[^A-Za-z]+", ' ', str(value["text"]).lower()))
            elif y<=2019:
                pre_cleaning5.append(re.sub("[^A-Za-z]+", ' ', str(value["text"]).lower()))
        except:
            print("Except 1", c)
        if c%100000==0:
            print(c)
        c+=1
    brief_cleaning = tuple(pre_cleaning1)
    with open(f"{category}_brief_cleaning_2012", "wb") as f:
        pickle.dump(brief_cleaning, f)
    brief_cleaning = tuple(pre_cleaning2)
    with open(f"{category}_brief_cleaning_2015", "wb") as f:
        pickle.dump(brief_cleaning, f)
    brief_cleaning = tuple(pre_cleaning3)
    with open(f"{category}_brief_cleaning_2017", "wb") as f:
        pickle.dump(brief_cleaning, f)
    brief_cleaning = tuple(pre_cleaning4)
    with open(f"{category}_brief_cleaning_2018", "wb") as f:
        pickle.dump(brief_cleaning, f)
    brief_cleaning = tuple(pre_cleaning5)
    with open(f"{category}_brief_cleaning_2019", "wb") as f:
        pickle.dump(brief_cleaning, f)
    """        
    for year in years:
        with open(f"{category}_brief_cleaning_{year}", "rb") as f:
            brief_cleaning = pickle.load(f)
        print(f"{category}_brief_cleaning_{year}")
        t = time()
    #	p = Pool(64)
    #	c = 0
    #	for_clean = []
    #	for i in nlp.pipe(brief_cleaning):
    #		for_clean.append(i)
    #		if c%10000==0:
    #			print(c)
    #		c+=1
        #for_clean = list(nlp.pipe(brief_cleaning))
        #print("list")
    #	txt = p.imap(cleaning, for_clean)
        txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=32, n_threads=-1)]
        print("txt completed in", time()-t, "with size", len(txt))
        with open(f"{category}_clean_{year}.txt", "wb") as f:
            pickle.dump(tuple(txt), f)
        """
        print("pua_clean completed in", time()-t)
        df_clean = pd.DataFrame({'clean': txt})
        df_clean = df_clean.dropna().drop_duplicates()
        df_clean.to_pickle(f"{category}.sqlite_clean.csv")
        for text, id_c in zip(txt, pua.keys()):
            pua_clean[id_c] = {"text":text, "timestamp":pua[id_c]["timestamp"]}
        print("pua_clean completed in", time()-t)
        pua.close()
        pua_clean.commit()
        print(f"{category}_ clean.sqlite commited")
        pua_clean.close()




        print(f"{category}.sqlite_clean.csv created")
        """
