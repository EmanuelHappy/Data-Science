__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import argparse
from time import time
import pandas as pd
import pickle
from multiprocessing import Pool
from sqlitedict import SqliteDict
from textblob import TextBlob

parser = argparse.ArgumentParser(description="""This script creates pickle objects to store text_blob values.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../sentiment/text_blob/data/",
                    help="Where to save the output files.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin at each split.")

parser.add_argument("--j", dest="j", type=int, default="0",
                    help="Split where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="-1",
                    help="Finish the program when reaches end.")

parser.add_argument("--commit", dest="commit", type=int, default="1000000",
                    help="Commit at some number of iterations.")

args = parser.parse_args()

splits = [i*10000000 for i in range(args.j, args.j+1)]


def multi_process(text):
    s = TextBlob(text)
    try:
        t = (s.sentiment[0], s.sentiment[1])
    except:
        t = (0, 0)
     
    return t


def add_blob(db1, j):
    t_ini = time()
    c = 0
    text_list = []
    id_list = []
    pol = []
    subj = []
    
    for id_c, values in db1.items():
        c += 1
        
        if c < args.init:
            continue

        text = values['text']
        text_list.append(text)
        id_list.append(id_c)
        if c % args.commit == 0:
            print(f'Iteration number {c} at {round((time()-t_ini)/ 60, 2)}')
            list_tuples = p.imap(multi_process, text_list)
            pp, ss = zip(*list_tuples)
            pol.extend(pp)
            subj.extend(ss)
            del text_list, pp, ss
            text_list = []
        
        if c == args.end:
            break

    with open(f"{args.dst}_{j}_{c}_pol", "wb") as f:
        pickle.dump(tuple(pol), f, protocol=4)
    with open(f"{args.dst}_{j}_{c}_subj", "wb") as f:
        pickle.dump(tuple(subj), f, protocol=4)
    with open(f"{args.dst}_{j}_{c}_id_list", "wb") as f:
        pickle.dump(tuple(id_list), f, protocol=4)
    df = pd.DataFrame({'id': id_list, 'polarity': pol, "subjective": subj})
    df.to_pickle(f"{args.dst}_{j}_{c}.csv")

    del text_list, id_list


if __name__ == '__main__':
    print("Start")
    p = Pool(7)
    
    time_init = time()
    for num in splits:
        print(num)
        dict_c = SqliteDict(f"./split_texts/text_dict_{num}.sqlite", tablename="value", flag="r")
        add_blob(dict_c, num//10000000)
        print(f"{num} finished at {time()-time_init}")
    
    time_end = time()
    print(f"Time to finish the analysis: {round((time_end-time_init) / 60, 2)}")

