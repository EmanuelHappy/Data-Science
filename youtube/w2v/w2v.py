import re
import pandas as pd
import spacy
import numpy as np
from sqlitedict import SqliteDict
from time import time
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
		print("Except")
		return ' '

categories = ["Intellectual Dark Web"]

for category in categories:
	print(f"Category = {category}")
	
	"""pua = SqliteDict(f"./../Sqlite/split_texts/{category}.sqlite", tablename="value", flag="r")"""

	pua_clean = SqliteDict(f"{category}_clean.sqlite", tablename="value", journal_mode="OFF")

	"""pre_cleaning = []
	for value in pua.values():
		try:
			pre_cleaning.append(re.sub("[^A-Za-z]+", ' ', str(value["text"]).lower()))
		except:
			print("Except 1")
			pre_cleaning.append(" ")
	brief_cleaning = tuple(pre_cleaning)
	with open("IDW_brief_cleaning", "wb") as f:
		pickle.dump(brief_cleaning, f)"""
	with open("IDW_brief_cleaning", "rb") as f:
		brief_cleaning = pickle.load(f)
	print("Brief_cleaning")
	t = time()
	txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=32, n_threads=16)]
	print("txt completed in", time()-t)
	for text, id_c in zip(txt, pua.keys()):
		pua_clean[id_c] = {"text":text, "timestamp":pua[id_c]["timestamp"]}
	t2 = time()
	print("pua_clean completed in", t2-t)
	pua.close()
	pua_clean.commit()
	print(f"{category}_ clean.sqlite commited")
	pua_clean.close()

	df_clean = pd.DataFrame({'clean': txt})

	df_clean = df_clean.dropna().drop_duplicates()

	df_clean.to_pickle(f"{category}.sqlite_clean.csv")

	print(f"{category}.sqlite_clean.csv created")

