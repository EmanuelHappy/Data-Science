__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import argparse
from multiprocessing import Pool
from time import time
from sqlitedict import SqliteDict
from empath import Empath

lexicon = Empath()

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on empath scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="empath_perspective_value.sqlite",
                    help="Where to save the output files.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="-1",
                    help="Comment where the analysis end.")

parser.add_argument("--commit", dest="commit", type=int, default="100000",
                    help="Commit at some number of iterations.")

args = parser.parse_args()

emotion_list = ['sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']

def multi_process(text):
    d = dict()
    d['lenght'] = len(text.split())
    a = lexicon.analyze(text, normalize=True)
    for emotion in emotion_list:
        d[emotion] = a[emotion]        
    
    return d

def add_empath(db1, db2):
    c = 0
    text_list = []
    id_list = []
    
    for id_c, values in db1.items():

        c+=1
        
        if c < args.init:
            continue

        text = values['text']
        text_list.append(text)
        id_list.append(id_c)

        if c % args.commit == 0:
            
            dict_list = p.map(multi_process, text_list)
            for i in range(len(id_list)):
                db2[id_list[i]] = dict_list[i]
            
            print(f'Iteration number {c} commited')
            db2.commit()
            del text_list, id_list
            text_list = []
            id_list = []
            
            
        if c==args.end:
            dict_list = p.map(multi_process, text_list)
            for i in range(len(id_list)):
                db2[id_list[i]] = dict_list[i]
                
            db2.commit()
            db2.close()
            return None


if __name__ == '__main__':
    
    p = Pool(16)

    time_init = time()
    dict_c = SqliteDict(args.src, tablename="text", flag="r")
    value_dict = SqliteDict(args.dst, tablename="value", journal_mode='OFF')
    
    add_empath(dict_c, value_dict)
    
    time_end = time()
    print(f"Time to finish the analysis: {round((time_end-time_init) / 60, 2)}")

    