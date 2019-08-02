__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import json
import argparse

from googleapiclient import discovery
from requests import Session
from multiprocessing import Pool
from time import time
from sqlitedict import SqliteDict
from empath import Empath

lexicon = Empath()

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on perspective API scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="perspective_value.sqlite",
                    help="Sqlite DataBase to store the perspective values.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="-1",
                    help="Comment where the analysis end.")

args = parser.parse_args()

# Parameters for the perspective api

attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT',
             'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT',  'FLIRTATION']

dict_attributes = {'TOXICITY' :{}, 'SEVERE_TOXICITY':{}, 'IDENTITY_ATTACK':{}, 'INSULT':{},
             'PROFANITY':{}, 'THREAT':{}, 'SEXUALLY_EXPLICIT':{},  'FLIRTATION':{}}

data_dict = {'comment': {'text': ''},
             'languages': ['en'],
             'requestedAttributes': dict_attributes}


def initialize_worker():
    """
    Initialize global session for the pools
    :return:
    """
    global session_global
    session_global = Session()


def process_text(text):
    """
    Make a perspective request for the text in parallel
    :param text: String that will be analysed by the perspective api
    :return: Dictionary with the request values
    """
    perspective_values = dict()
    data_dict['comment']['text'] = text

    session = session_global
    response = session.post(url=url, json=data_dict)

    # The following part was added to slow the # of requests/second, so I can increase the # of multi-processing workers
    
    response_dict = json.loads(response.content)
    
    try:
        for attr in attributes:
            perspective_values[attr] = response_dict['attributeScores'][attr]['summaryScore']['value']
    except:
        print(text)
        print(response)
        print(response_dict)
        
    return perspective_values

    
def add_perspective(db1, db2):
    """
    Store in the output Database the values of the perspective api for each comment in the input Database
    :param db1: Input Database
    :param db2: Output Database
    :return: None
    """
    c = 0
    jsons_to_load = []
    id_list = []

    for id_c, values in db1.items():
        
        c += 1
        if c < args.init:
            continue      
            
        id_list.append(id_c)

        jsons_to_load.append(values['text'])
        
        if c == args.end:

            print('Requests initiated')
            t_req_i = time()

            perspective_list = p.map(process_text, jsons_to_load)

            t_req_e = time()
            print(f"Time to finish the requests: {round((t_req_e-t_req_i) / 60, 2)}")

            for id_c_out, perspective_value in zip(id_list, perspective_list):
                db2[id_c_out] = perspective_value

            db2.commit()
            db2.close()
            
            return None

    
if __name__ == '__main__':

    print('start')  # FeedBack

    # Loading API KEY:
    with open('secrets.json') as file:
        api_key = json.load(file)['key']

    #  Connecting to the API:
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' + '?key=' + api_key)
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=api_key)

    # Initiating the DataBases:
    dict_c = SqliteDict(args.src, tablename="text", flag="r")
    value_dict = SqliteDict(args.dst, tablename="value", journal_mode='OFF')

    # Initiating multi-process pool:
    workers = 20  # The number 20 was chosen because it best fit the # of requests/second
    p = Pool(workers, initializer=initialize_worker)
    
    time_init = time()

    # Running Perspective
    add_perspective(dict_c, value_dict)

    # FeedBack at the end
    time_end = time()
    print(f"Time to finish the analysis: {round((time_end-time_init) / 60, 2)}")
