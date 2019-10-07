import pandas as pd
import pickle
from sqlitedict import SqliteDict
import numpy as np
from datetime import datetime
from time import time
import itertools

name = "control"
names_control = ["right-center", "center", "left", "left-center", "right1", "right2"]
names_list = ["control"]

emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']
attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT',
              'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT', 'FLIRTATION']


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
        u_pval = (1 + p) / 2.
        l_pval = (1 - u_pval)
        l_indx = int(np.floor(n * l_pval))
        u_indx = int(np.floor(n * u_pval))
        return (simulations[l_indx], simulations[u_indx])

    return (ci)


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

filenames = ["0_5000000", "0_10000000", "0_15000000", "0_20000001", "2?2_285042", "2?3_887730", "2?4_6000000",
             "2?_640000", "2_2390000", "3.1_2180000", "3_7900000", "4.1_4581097", "4.2_320000", "4.3_1050000",
             "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]

ide = []
pol = []

for fname in filenames:
    print(fname)
    p2 = []
    id2 = []
    with open(f"./perspective/perspective_{fname}_val", "rb") as fp:
        persp1 = pickle.load(fp)
    with open(f"./perspective/perspective_{fname}_id", "rb") as fp:
        ide1 = pickle.load(fp)
    ide1 = np.array(ide1)
    for i in range(len(persp1)):
        if len(persp1[i]) == 0:
            continue
        p2.append(np.array([*persp1[i]]))
        id2.append(ide1[i])

    ide.extend(id2)
    pol.extend(p2)
    print(f"len pers = {len(pol)}, len ide = {len(ide)}")

print(f"type persp[0] = {type(pol[0])}, shape = {pol[0].shape}")
d_persp = dict(zip(ide, pol))
print("d_persp", len(d_persp))
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

    # d_subj = dict(zip(ide, sub))
    # print("d_sub")
    d["year"] = [i for i in range(2010, 2020)]

    for attri in range(len(attributes)):
        y_emotion = []
        dif = 0.1
        d = {}
        for emotion in emotion_list[1:]:
            d[emotion] = []
            d[f"{emotion}_dyu"] = []
            d[f"{emotion}_dyd"] = []
            d[f"{emotion}_std"] = []
            print(name, attributes[attri], emotion)
            y_mean = []
            pos = []
            neu = []
            neg = []
            y = []
            for i in range(2010, 2020):
                y1 = []
                    
                with open(f"./empath_blob/{name}_empath_{emotion}_{i}", "rb") as f:
                    keys = pickle.load(f)
                if(name=="control" and emotion=="positive_emotion" and i==2019):
                    keys = np.delete(keys, 135957)
                    keys = np.delete(keys, 491363)
                    keys = np.delete(keys, 651421)
                if(name=="control" and emotion=="masculine" and i==2018):
                    keys = np.delete(keys, 529173)

                for key in keys:
                    if key in d_persp:
                        y1.append(d_persp[key][attri])
                y.append(np.array(y1))
            y_mean = []
            y_std = []
            dyu = []
            dyd = []
            count=2010
            for i in y:
                y_mean.append(np.mean(i))
                y_std.append(np.std(i))
                boot = bootstrap(i)
                c = boot(.95)
                if(count>2017):
                    print(count, c)
                count+=1
                dyd.append(c[0])
                dyu.append(c[1])
            d[emotion] = y_mean
            d[f"{emotion}_dyu"] = dyu
            d[f"{emotion}_dyd"] = dyd
            d[f"{emotion}_std"] = y_std


        df = pd.DataFrame(d)
        # df = pd.DataFrame({"x":x, "y":y_mean, "std":y_std})
        df.to_csv(f"./empath_perspective/{name}_{attributes[attri]}_empath.csv")

        # pos.append(np.sum(np.array(y)>dif)/len(np.array(y)))
        # neg.append(np.sum(np.array(y)<-dif)/len(np.array(y)))
        # neu.append(1-pos[-1]-neg[-1])
        # y_emotion.append((np.array(neg), np.array(neu), np.array(pos)))
        # print(len(y_emotion), len(pos), len(y))
        # with open(f"./empath_blob/{name}_pol_empath_prop", "wb") as f:
        #    pickle.dump(y_emotion, f)

