from sqlitedict import SqliteDict
from empath import Empath
import copy

lexicon = Empath()

path_db = "/../../../scratch/manoelribeiro/helpers/text_dict.sqlite"
emotion_list= ['sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']

import json
import requests
from googleapiclient import discovery

with open('secrets.json') as file:
    api_key = json.load(file)['key']
    
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +
       '?key=' + api_key)

attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT',
             'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT',  'FLIRTATION']

dict_attributes = {'TOXICITY' :{}, 'SEVERE_TOXICITY':{}, 'IDENTITY_ATTACK':{}, 'INSULT':{},
             'PROFANITY':{}, 'THREAT':{}, 'SEXUALLY_EXPLICIT':{},  'FLIRTATION':{}}
values = {}

service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=api_key)

from requests import Session
from multiprocessing import Pool


def initialize_worker():
    global session_global
    session_global = Session()
    
def process_json(input):

    # call Perspective api here
    session = session_global
    return session.post(url=url, json=input)

def add_perspective(db1, db2):
    c = 0
    jsons_to_load = []
    id_list = []
    
    data_dict = {'comment': {'text': ''},
                 'languages': ['en'],
                'requestedAttributes': dict_attributes}

    for id_c, values in db1.items():
        
        c+=1
        if c < args.init:
            continue
            
            
        id_list.append(id_c)
        

        data_dict['comment']['text'] = values['text']

        jsons_to_load.append(copy.deepcopy(data_dict))

        
        if c == args.end:
            response_list = p.map(process_json, jsons_to_load)
            print(response_list)
            for i in range(len(id_list)):
                
                perspective_values = dict()
                id_c = id_list[i]
                response = response_list[i]
                
                response_dict = json.loads(response.content)['attributeScores']

                for attr in attributes:
                    perspective_values[attr] = response_dict[attr]['summaryScore']['value']
                
                db2[id_c] = perspective_values 
                #print(id_c, db2[id_c])
        

            db2.commit()
            db2.close()
            
            return

p = Pool(12, initializer=initialize_worker)

dict_c = SqliteDict(path_db, tablename="text", flag="r")     
new_dict = SqliteDict("perspective_value.sqlite", tablename="value")

add_perspective(dict_c, new_dict)