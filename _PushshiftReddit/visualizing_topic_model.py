__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import pickle
from gensim.models import CoherenceModel, HdpModel
from gensim.corpora import Dictionary, MmCorpus
import pyLDAvis.gensim
import warnings
warnings.filterwarnings('ignore')  # Let's clean the output

hdpmodel = HdpModel.load('hdp_model_spacy.gensim')
dictionary = Dictionary.load('hdp_dictionary.dict')
corpus = MmCorpus('hdp_corpus.mm')
with open("texts.txt", "rb") as fp:   # Unpickling
    texts = pickle.load(fp)

print("Files loaded")

topic_info = hdpmodel.print_topics()
for topic in topic_info:
    print(topic)

vis_hdpmodel = hdpmodel.suggested_lda_model()

vis_hdp = [[word for word, prob in topic] for topicid, topic in vis_hdpmodel.show_topics(formatted=False)]

coherence = CoherenceModel(topics=vis_hdp[:10], texts=texts, dictionary=dictionary, window_size=10).get_coherence()
print(f" The coherence of the top 10 lda suggest model is {coherence}")

p = pyLDAvis.gensim.prepare(vis_hdpmodel, corpus, dictionary)
pyLDAvis.save_html(p, 'topic_model.html')
print("pyLDAvis saved as topic_model.html")
