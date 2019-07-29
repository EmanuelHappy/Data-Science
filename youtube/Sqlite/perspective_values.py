__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import json
import requests
import argparse
import gc

from googleapiclient import discovery
from time import time
from sqlitedict import SqliteDict
from empath import Empath

lexicon = Empath()

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on empath scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="perspective_value.sqlite",
                    help="Where to save the output files.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="-1",
                    help="Comment where the analysis end.")

parser.add_argument("--commit", dest="commit", type=int, default="10000",
                    help="Commit at some number of iterations.")

parser.add_argument("--del", dest="del", type=int, default="5",
                    help="Free memory at this number of iterations.")

args = parser.parse_args()


attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT',
             'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT',  'FLIRTATION']

dict_attributes = {'TOXICITY' :{}, 'SEVERE_TOXICITY':{}, 'IDENTITY_ATTACK':{}, 'INSULT':{},
             'PROFANITY':{}, 'THREAT':{}, 'SEXUALLY_EXPLICIT':{},  'FLIRTATION':{}}



def add_perspective(db1, db2, url):
    c = 0
    
    data_dict = {'comment': {'text': ''},
                 'languages': ['en'],
                'requestedAttributes': dict_attributes}

    for id_c, values in db1.items():
        c+=1
        
        if c < args.init:
            continue
    
        print(c)
        
        perspective_values = dict()

        data_dict['comment']['text'] = values['text']

        response = requests.post(url=url, data=json.dumps(data_dict))
        response_dict = json.loads(response.content)
        
        for attr in attributes:
            perspective_values[attr] = response_dict['attributeScores'][attr]['summaryScore']['value']

        db2[id_c] = perspective_values 
        
        if c % args.commit == 0:
            print(f'Iteration number {c} commited')
            db2.commit()
            
        if c == args.end:
            break     
        
    db2.commit()
    db2.close()

    
if __name__ == '__main__':
    
    

    with open('secrets.json') as file:
        api_key = json.load(file)['key']
    
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +
       '?key=' + api_key)
    
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=api_key)
    
    dict_c = SqliteDict(args.src, tablename="text", flag="r")
    value_dict = SqliteDict(args.dst, tablename="value", journal_mode='OFF')
    
    time_init = time()
    
    add_perspective(dict_c, value_dict, url)
    
    time_end = time()
    print(f"Time to finish the analysis: {round((time_end-time_init) / 60, 2)}")

    