import matplotlib.pyplot as plt
import gensim
import numpy as np
import pandas as pd
import spacy
import pickle 

from gensim.models.wrappers.dtmmodel import DtmModel
from gensim.models import CoherenceModel, LdaModel, LsiModel, HdpModel
from gensim.models.wrappers import LdaMallet
from gensim.corpora import Dictionary, MmCorpus

sub = "Alt-lite"
years = [2012, 2015, 2017, 2018, 2019]
time_seq = []
sub_sentences=[]
c = 0
for year in years:
    print(year)
    with open(f"./../w2v/{sub}_sentences_{year}.txt", "rb") as fp:  # 
        sub_sentences2 = pickle.load(fp)
        sub_sentences.extend(sub_sentences2)
        time_seq.append(len(sub_sentences2))
print(time_seq)
with open(f"./data/{sub}_time_seq.txt", "wb") as fb:  # 
      pickle.dump(time_seq, fb)
with open(f"./data/{sub}_sentences.txt", "wb") as fp:  # 
      pickle.dump(sub_sentences, fp, protocol=4)
print(f"{sub} sentences saved")
PUA_dict = Dictionary(sub_sentences)
PUA_dict.save(f"./data/{sub}_hdp_dictionary.dict")
print(f"{sub} Dictionary saved as {sub}_hdp_dictionary.dict")
PUA_corpus = [PUA_dict.doc2bow(text) for text in sub_sentences]
MmCorpus.serialize(f'./data/{sub}_hdp_corpus.mm', PUA_corpus)
print(f'Corpus saved as {sub}_hdp_corpus.mm')

"""
dtm_path = "./../../_PushshiftReddit/topic_model/data/dtm/dtm-linux64"
PUA_model = DtmModel(dtm_path, PUA_corpus, time_seq, num_topics=10,
                 id2word=PUA_dict, initialize_lda=True, alpha=0.1)
print("Model created")
PUA_model.save(f"./lda/{sub}_dtm.gensim")
exit()
i = input()

for i in sub_sentences:
    print(i)
print(sub_sentences)
i = input()
for year in years:
    with open(f"./../w2v/{sub}_sentences_{year}.txt", "rb") as fp:  # Pickling
        sub_sentences = pickle.load(fp)
    
    i = input()
    print(f'{sub}_sentences_{year}.txt loaded')

    dictionary = Dictionary(sub_sentences)
    dictionary.save(f"./data/{sub}_hdp_dictionary_{year}.dict")

    print(f"{sub} Dictionary saved as {sub}_hdp_dictionary_{year}.dict")
    corpus = [dictionary.doc2bow(text) for text in sub_sentences]
    MmCorpus.serialize(f'./data/{sub}_hdp_corpus_{year}.mm', corpus)
    print(f'Corpus saved as {sub}_hdp_corpus_{year}.mm')
    
from gensim.models.wrappers.dtmmodel import DtmModel
PUA_corpus = MmCorpus(f'./data/{sub}_hdp_corpus.mm')
PUA_dict =  Dictionary.load(f'./data/{sub}_hdp_dictionary.dict')
#for year in years:
#    c = MmCorpus(f'./data/PUA_hdp_corpus_{year}.mm')
#    PUA_time_seq.append(len(c))
dtm_path = "./../../_PushshiftReddit/topic_model/data/dtm/dtm-linux64"
PUA_model = DtmModel(dtm_path, PUA_corpus, PUA_time_seq, num_topics=10,
                 id2word=PUA_dict, initialize_lda=True, alpha=0.1)
PUA_model.save("./lda/PUA_dtm.gensim")
"""    
    
    
    
    
    