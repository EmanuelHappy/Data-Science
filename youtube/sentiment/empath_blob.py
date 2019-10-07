import pandas as pd
import pickle
from sqlitedict import SqliteDict
import numpy as np
from datetime import datetime
from time import time
import itertools

name = "control"
names_control = ["right-center", "center", "left", "left-center", "right1", "right2"]
names_list = ["Alt-right", "IDW", "Alt-lite", "control"]

emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']

attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT',
             'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT',  'FLIRTATION']

def bootstrap(data, n=1000, func=np.mean):
    """
    Generate `n` bootstrap samples, evaluating `func`
    at each resampling. `bootstrap` returns a function,
    which can be called to obtain confidence intervals
    of interest.
    """
    simulations = list()
    sample_size = len(data)
    xbar_init = np.mean(data)
    for c in range(n):
        itersample = np.random.choice(data, size=sample_size, replace=True)
        simulations.append(func(itersample))
    simulations.sort()
    def ci(p):
        """
        Return 2-sided symmetric confidence interval specified
        by p.
        """
        u_pval = (1+p)/2.
        l_pval = (1-u_pval)
        l_indx = int(np.floor(n*l_pval))
        u_indx = int(np.floor(n*u_pval))
        return(simulations[l_indx],simulations[u_indx])
    return(ci)

"""
d_year={2006:{}, 2007:{}, 2008:{}, 2009:{}, 2010:{}, 2011:{}, 2012:{}, 2013:{}, 2014:{}, 2015:{}, 2016:{}, 2017:{}, 2018:{}, 2019:{}}
d_empath = {}
for emotion in emotion_list:
    d_empath[emotion] = {}
    for year in range(2006, 2020):
        d_empath[emotion][year] = [] 
    
for name in names_control:
    with open(f"{name}.pickle", "rb") as fp:
        ks = pickle.load(fp)

    filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000"]
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
                for j in range(1, len(emotion_list)):
                    if empath[i][j] > 0:
                        d_empath[emotion_list[j]][ks[key]].append(key)


        print(fname, "sadness", len(d_empath["sadness"][2018]))
        print(fname, "positive", len(d_empath["positive_emotion"][2018]))
"""
ide = []
pol = []

filenames = ["n", "1_10000000", "2_10000000", "3_10000000", "4_10000000", "5_10000000", "6_10000000", "7_4989623"]

for fname in filenames:

    if fname!="n":
        with open(f"blobm_{fname}_pol", "rb") as fp:
            pol1 = pickle.load(fp)
        print("pol")
        with open(f"blobm_{fname}_id_list", "rb") as fp:
            ide1 = pickle.load(fp)
    else:
        with open(f"blob_{fname}_pol", "rb") as fp:
            pol1 = pickle.load(fp)
        print("pol")
        with open(f"blob_{fname}_id", "rb") as fp:
            ide1 = pickle.load(fp)
    ide.extend(ide1)
    pol.extend(pol1)
    print(len(pol), len(ide))
d_pol = dict(zip(ide, pol))
print("d_pol", len(d_pol))
for name in names_list:
    print(name)

    """    
    with open(f"blobm_6_10000000_pol", "rb") as f:
        test2 = pickle.load(f)
    d = dict(zip(test, test2))
    with open(f"./empath_blob/Alt-lite_empath_negative_emotion_2018", "rb") as f:
        keys = pickle.load(f)
    for key in keys:
        if key in d:
            print(key)

    with open(f"blob_n_id", "rb") as f:
        ide = pickle.load(f)
    print("id")
    with open(f"blob_n_pol", "rb") as f:
        pol = pickle.load(f)
    print("pol")
    #with open(f"blob_n_sub", "rb") as f:
    #    sub = pickle.load(f)
    #print("sub")"""

    #d_subj = dict(zip(ide, sub))
    #print("d_sub")
    y_emotion = []
    dif=0.1
    d = {}
    for emotion in emotion_list[1:]:
        d[emotion] = []
        d[f"{emotion}_dyu"] = []
        d[f"{emotion}_dyd"] = [] 
        d[f"{emotion}_std"] = [] 
        print(emotion)
        y_mean = []
        pos = []
        neu = []
        neg = []
        y=[]
        for i in range(2007, 2020):
            y1 = []
            with open(f"./empath_blob/{name}_empath_{emotion}_{i}", "rb") as f:
                keys = pickle.load(f)
            for key in keys:
                if key in d_pol:
                    y1.append(d_pol[key])
            y.append(np.array(y1))
        print(len(y), y[0])
        y_mean = []
        y_std = []
        dyu = []
        dyd = []
        for i in y:
            y_mean.append(np.mean(i))
            y_std.append(np.std(i))
            boot = bootstrap(i)
            c = boot(.95)
            print(c)
            dyd.append(c[0])
            dyu.append(c[1])
        d[emotion] = y_mean
        d[f"{emotion}_dyu"] = dyu
        d[f"{emotion}_dyd"] = dyd
        d[f"{emotion}_std"] = y_std
        
    d["year"] = [i for i in range(2007, 2020)]
        
    df = pd.DataFrame(d)
    #df = pd.DataFrame({"x":x, "y":y_mean, "std":y_std})
    df.to_csv(f"./empath_blob/{name}_pol_empath_prop_boots.csv")

            #pos.append(np.sum(np.array(y)>dif)/len(np.array(y)))
            #neg.append(np.sum(np.array(y)<-dif)/len(np.array(y)))
            #neu.append(1-pos[-1]-neg[-1])
        #y_emotion.append((np.array(neg), np.array(neu), np.array(pos)))
        #print(len(y_emotion), len(pos), len(y))
    #with open(f"./empath_blob/{name}_pol_empath_prop", "wb") as f:
    #    pickle.dump(y_emotion, f)

    