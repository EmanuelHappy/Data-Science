import pandas as pd
#import cPickle as pickle
import pickle
from sqlitedict import SqliteDict
import numpy as np
from datetime import datetime

from time import time

name = "Alt-lite"
"""
t = time()
#alt_right = SqliteDict(f"/../../../scratch/manoelribeiro/helpers/text_dict.sqlite", tablename="text", flag="r")
alt_right = SqliteDict(f"./../Sqlite/split_texts/{name}.sqlite", tablename="value", flag="r")
ks = {}
years = []
c = 0
for key, value in alt_right.items():
    if c% 1000000 == 0:
        print(c)
    c+=1
    if c>20000000:
        break
    #if value["category"]!='right':
    #    continue

    ks[key] = datetime.fromtimestamp(value["timestamp"]//1000).year
    #ks[key] = value["timestamp"]
print(time()-t)

#alt_right.close()

with open(f'{name}.pickle', 'wb') as handle:
    pickle.dump(ks, handle, protocol=pickle.HIGHEST_PROTOCOL)
print("pickle")
exit()
"""
with open(f"{name}.pickle", "rb") as fp:
    ks = pickle.load(fp)

d_pol={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
d_subj={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
filenames = ["3_10000000", "4_10000000", "5_10000000", "6_10000000", "7_4989623"]

for fname in filenames:
    with open(f"blobm_{fname}_subj", "rb") as fp:
        subj = pickle.load(fp)
    print("subj")
    with open(f"blobm_{fname}_pol", "rb") as fp:
        pol = pickle.load(fp)
    print("pol")
    with open(f"blobm_{fname}_id_list", "rb") as fp:
        ide = pickle.load(fp)   
    print("id")

    for i in range(len(pol)):
        if i%1000000==0:
            print(i)
        key = ide[i]
        if key in ks:
            #dt_object = datetime.fromtimestamp(ks[key]//1000)
            d_pol[ks[key]].append(pol[i])
            d_subj[ks[key]].append(subj[i])
        
    print(fname, len(d_pol[2018]))

for i in range(2007, 2020):
    print(i)
    with open(f"{name}_pol_{i}", "wb") as f:
        pickle.dump(tuple(np.array(d_pol[i])), f, protocol=4)
    with open(f"{name}_subj_{i}", "wb") as f:
        pickle.dump(tuple(np.array(d_subj[i])), f, protocol=4)
                    
"""
with open("blobm_3_10000000_subj", "rb") as fp:
    subj4 = pickle.load(fp)
print("subj")
with open("blobm_3_10000000_id_list", "rb") as fp:
    id4 = pickle.load(fp)   
    
print("id")
d_pol={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
d_subj={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
for i in range(len(subj4)):
    if i%1000000==0:
        print(i)
    key = id4[i]
    if key in ks:
        #dt_object = datetime.fromtimestamp(ks[key]//1000)
        #d_pol[ks[key]].append(pol4[i])
        #d_subj[ks[key]].append(subj4[i])
        #d_pol[dt_object.year].append(pol4[i])
        d_subj[ks[key]].append(subj4[i])
        
print(4, len(d_subj[2019]))

with open("blobm_4_10000000_subj", "rb") as fp:
    subj4 = pickle.load(fp)
print("subj")
with open("blobm_4_10000000_id_list", "rb") as fp:
    id4 = pickle.load(fp)    
print("id")

for i in range(len(subj4)):
    if i%1000000==0:
        print(i)
    key = id4[i]
    if key in ks:
        #dt_object = datetime.fromtimestamp(ks[key]//1000)
        #d_pol[ks[key]].append(pol4[i])
        #d_subj[ks[key]].append(subj4[i])
        #d_pol[dt_object.year].append(pol4[i])
        d_subj[ks[key]].append(subj4[i])
        
print(3, len(d_subj[2019]))

for i in range(2007, 2020):
    print(i)
    with open(f"{name}_subj_{i}", "wb") as f:
        pickle.dump(tuple(np.array(d_subj[i])), f, protocol=4)
"""