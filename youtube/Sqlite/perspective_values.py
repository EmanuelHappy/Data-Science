__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import json
import argparse
import gc
import copy

from googleapiclient import discovery
from requests import Session
from multiprocessing import Pool
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

data_dict = {'comment': {'text': ''},
             'languages': ['en'],
             'requestedAttributes': dict_attributes}

def initialize_worker():
    global session_global
    session_global = Session()
    
def process_json(text):
    perspective_values = dict()
    data_dict['comment']['text'] = text
    session = session_global
    response = session.post(url=url, json=data_dict)
    
    response_dict = json.loads(response.content)
     
    for attr in attributes:
        perspective_values[attr] = response_dict['attributeScores'][attr]['summaryScore']['value']
        
    return perspective_values

def multi_attr(response):
    perspective_values = dict()
    response_dict = json.loads(response.content)
    
    for attr in attributes:
        perspective_values[attr] = response_dict['attributeScores'][attr]['summaryScore']['value']
        
    return perspective_values
        
    
def add_perspective(db1, db2):
    c = 0
    jsons_to_load = []
    id_list = []

    for id_c, values in db1.items():
        
        c+=1
        if c < args.init:
            continue      
            
        id_list.append(id_c)

        jsons_to_load.append(values['text'])
        
        if c == args.end:
            print('start requests')
            t_req_i = time()
            perspective_list = p.map(process_json, jsons_to_load)
            t_req_e = time()
            print(f"Time to finish the request: {round((t_req_e-t_req_i) / 60, 2)}")
            
            
            for id_c, perspective_value in zip(id_list, perspective_list):
                db2[id_c] = perspective_value

            db2.commit()
            db2.close()
            
            return None

    
if __name__ == '__main__':
    print('start')
    with open('secrets.json') as file:
        api_key = json.load(file)['key']
    
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +
       '?key=' + api_key)
    
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=api_key)
    
    dict_c = SqliteDict(args.src, tablename="text", flag="r")
    value_dict = SqliteDict(args.dst, tablename="value", journal_mode='OFF')
    
    p = Pool(20, initializer=initialize_worker)
    p2 = Pool(16)
    
    time_init = time()
    
    add_perspective(dict_c, value_dict)
    
    time_end = time()
    print(f"Time to finish the analysis: {round((time_end-time_init) / 60, 2)}")

    