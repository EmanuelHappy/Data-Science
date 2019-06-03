__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import gensim
import pandas as pd
import spacy
import pickle

from gensim.models import CoherenceModel, HdpModel
from gensim.corpora import Dictionary, MmCorpus

sdf = pd.read_csv('subreddits.csv')
subreddits = sdf.values.tolist()

for s in subreddits:
    sub = str(s)[5:-5]

    temp_df = pd.read_csv(f'./data/reddit/cm/{sub}_comments.csv')
    temp_serie = temp_df.Comment
    if s == subreddits[0]:
        serie = temp_serie
    else:
        serie = temp_serie.append(temp_serie, ignore_index=True)

    print(f'Subreddit {sub} comments stored')

serie = serie[serie != '[deleted]']

serie.to_csv("./data/reddit/cm/all_comments.csv")
print('Created file with all comments')

nlp = spacy.load("en")

my_stop_words = [u'say', u'\s', u'Mr', u'be', u'said', u'says', u'saying', u's', u'’s', u'\n\n', u'\n', u' \n']
for stopword in my_stop_words:
    lexeme = nlp.vocab[stopword]
    lexeme.is_stop = True

stl = pd.Series.tolist(serie)

texts, article, skl_texts = [], [], []

count = 0
print("Comments cleaned: ")
for comment in stl:
    try:
        doc = nlp(comment)
    except:
        continue
    for w in doc:
        # if it's not a stop word or punctuation mark, add it to our article!
        if not w.is_stop and not w.is_punct and not w.like_num:
            # we add the lematized version of the word
            article.append(w.lemma_)
        # assume each comment as a document
        if w.text == doc[-1].text:
            skl_texts.append(' '.join(article))
            texts.append(article)
            article = []
    count += 1
    if count % 100000 == 0:
        print(count, end=' ')

with open("texts.txt", "wb") as fp:  # Pickling
    pickle.dump(texts, fp)
print('texts.csv created')

bigram = gensim.models.Phrases(texts)

dictionary = Dictionary(texts)
dictionary.save("hdp_dictionary.dict")
print("Dictionary saved as hdp_dictionary.dict")
corpus = [dictionary.doc2bow(text) for text in texts]
MmCorpus.serialize('hdp_corpus.mm', corpus)
print('Corpus saved as hdp_corpus.mm')

hdpmodel = HdpModel(corpus=corpus, id2word=dictionary)

hdpmodel.save('hdp_model_spacy.gensim')
print('hdp model created')

hdptopics = [[word for word, prob in topic] for topicid, topic in hdpmodel.show_topics(formatted=False)]

hdp_coherence = CoherenceModel(topics=hdptopics[:10], texts=texts,
                               dictionary=dictionary, window_size=10).get_coherence()

print(f"The topic coherence is {hdp_coherence}")
