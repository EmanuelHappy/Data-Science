import pandas as pd
import pickle
from sqlitedict import SqliteDict
import numpy as np
from datetime import datetime
from time import time
import itertools

name = "Alt-lite"

with open(f"{name}.pickle", "rb") as fp:
    ks = pickle.load(fp)

t = time()

#alt_right = SqliteDict(f"/../../../scratch/manoelribeiro/helpers/text_dict.sqlite", tablename="text", flag="r")
#alt_right = SqliteDict(f"./../Sqlite/split_texts/Alt-right.sqlite", tablename="value", flag="r")
ks = {}
years = []
c = 0
"""
for key, value in alt_right.items():
    if c% 1000000 == 0:
        print(c)
    c+=1
    if c>10000000:
        break
    #if value["category"]!='right':
    #    continue

    ks[key] = datetime.fromtimestamp(value["timestamp"]//1000).year
    #ks[key] = value["timestamp"]
"""
print(time()-t)

pers = "0"
p2 = SqliteDict(f"./perspective/perspective_value{pers}.sqlite", tablename="value", flag="r")

d_empath={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
ini=0
c = 15000000
t_ini = time()
ids = []
perspective = []
to_request = [(k, v) for k, v in itertools.islice(p2.items(), 15000001, 20000001)]

for key, value in to_request:

    if c%100000==0:
        print(c, round((time()-t_ini)/60, 2))
    c+=1

    if c%25000000==0:
        print(":D")
        #with open(f"./perspective/perspective_{pers}_{c}_val", "wb") as f:
        #    pickle.dump(np.array(perspective), f, protocol=4)
        print("Val")
        with open(f"./perspective/perspective_{pers}_{c}_id", "wb") as f:
            pickle.dump(tuple(np.array(ids)), f, protocol=4)
        print("ID")
        exit()
        
    ids.append(key)
    perspective.append(tuple(value.values()))
c+=1
print(":D")
with open(f"./perspective/perspective_{pers}_{c}_val", "wb") as f:
        pickle.dump(np.array(perspective), f, protocol=4)
print("Val")
with open(f"./perspective/perspective_{pers}_{c}_id", "wb") as f:
        pickle.dump(tuple(np.array(ids)), f, protocol=4)
print("ID")
"""    
d_emp={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
filenames = ["3.1_2180000", "3_7900000", "4.1_4581097", "4.2_320000", "4.3_1050000", "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]
for fname in filenames:
    with open(f"./perspective/perspective_{fname}_val", "rb") as fp:
        perspective = pickle.load(fp)
    print("perspective")
    with open(f"./perspective/perspective_{fname}_id", "rb") as fp:
        ide = pickle.load(fp)   
    print("id")

    for i in range(len(perspective)):
        if i%1000000==0:
            print(i)
        key = ide[i]
        if key in ks:
            #dt_object = datetime.fromtimestamp(ks[key]//1000)
            d_emp[ks[key]].append(perspective[i])
        
    print(fname, len(d_emp[2018]))

for i in range(2007, 2020):
    print(i)
    with open(f"./perspective/{name}1_perspective_{i} ", "wb") as f:
        pickle.dump(tuple(np.array(d_emp[i])), f, protocol=4)"""
