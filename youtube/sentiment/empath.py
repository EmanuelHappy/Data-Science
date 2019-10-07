import pandas as pd
import pickle
from sqlitedict import SqliteDict
import numpy as np
from datetime import datetime
from time import time
import itertools

name = "IDW"

"""
e2 = SqliteDict("empath_value6.sqlite", tablename="value", flag="r")

d_empath={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
ini=0
c = 0
t_ini = time()
ids = []
empath = []
#to_request = [(k, v) for k, v in itertools.islice(e2.items(), 40000001, 50000001)]
c = 0
for key, value in e2.items():
    if c%10000000==0:
        print(c, round((time()-t_ini)/60, 2))
    c+=1
    if c<50000000:
        continue
    if c%100000==0:
        print(c, round((time()-t_ini)/60, 2))
        
    ids.append(key)
    empath.append(tuple(value.values()))
        
print(":D")
with open(f"empath_6_{c}_val", "wb") as f:
        pickle.dump(np.array(empath), f, protocol=4)
print("Val")
with open(f"empath_6_{c}_id", "wb") as f:
        pickle.dump(tuple(np.array(ids)), f, protocol=4)
print("ID")

"""

with open(f"{name}.pickle", "rb") as fp:
    ks = pickle.load(fp)

d_emp={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
filenames = ["6_10000000", "6_20000000","6_30000000"]
for fname in filenames:
    with open(f"empath_{fname}_val", "rb") as fp:
        empath = pickle.load(fp)
    print("perspective")
    with open(f"empath_{fname}_id", "rb") as fp:
        ide = pickle.load(fp)   
    print("id")

    for i in range(len(empath)):
        if i%1000000==0:
            print(i)
        key = ide[i]
        if key in ks:
            #dt_object = datetime.fromtimestamp(ks[key]//1000)
            d_emp[ks[key]].append(empath[i])
        
    print(fname, len(d_emp[2018]))

for i in range(2007, 2020):
    print(i)
    with open(f"{name}_empath_{i}", "wb") as f:
        pickle.dump(tuple(np.array(d_emp[i])), f, protocol=4)
    
