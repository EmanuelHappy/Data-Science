__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import json
import argparse
import itertools

from googleapiclient import discovery
from requests import Session
from multiprocessing import Pool
from time import time, sleep
from sqlitedict import SqliteDict

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on perspective API scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../sentiment/perspective/data/sqlite/"
                                                           "perspective_value.sqlite",
                    help="Sqlite DataBase to store the perspective values.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="-1",
                    help="Comment where the analysis end.")

parser.add_argument("--loop", dest="loop", type=int, default="1",
                    help="Number of loops that perspective will be called."
                         "Correct: (end-init) / loop == 10000")

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
    d1 = time()
    to_request = [(k, v["text"]) for k, v in itertools.islice(db1.items(), args.init, args.end)]
    id_list, jsons_to_load = zip(*to_request)
    d2 = time()
    print(f"Len id_list = {len(id_list)}")

    dif = (args.end - args.init)//args.loop
    
    print(f"time to iterate: {round((d2-d1)/60, 2)}")
    print('Requests initiated')

    dt = d2 - d1
    for i in range(args.loop):
        if i != 0:
            if dt > 100:
                sleep(100)
            else:
                sleep(110-dt)
            
        t_req_i = time()
        if i != args.loop-1:
            perspective_list = p.map(process_text, jsons_to_load[dif*i : dif*(i+1)])
        else:
            perspective_list = p.map(process_text, jsons_to_load[dif*i:])

        t_req_e = time()
 
        if i != args.loop-1:
            for id_c_out, perspective_value in zip(id_list[dif*i : dif*(i+1)], perspective_list):
                db2[id_c_out] = perspective_value
        else:
            for id_c_out, perspective_value in zip(id_list[dif*i:], perspective_list):
                db2[id_c_out] = perspective_value

        db2.commit()
        dt = t_req_e - t_req_i
        print(f"Time to finish the {i+1} requests: {round(dt, 2)}")

    db2.commit()


if __name__ == '__main__':

    print('start')  # FeedBack

    # Loading API KEY:
    with open('secrets.json') as file:
        api_key = json.load(file)['key']

    #  Connecting to the API:
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' + '?key=' + api_key)
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=api_key)

    # Initiating the DataBases:
    dict_c = SqliteDict(args.src, tablename="value", flag="r")
    value_dict = SqliteDict(args.dst, tablename="value", journal_mode="OFF")

    # Initiating multi-process pool:
    workers = 50  # The number 20 was chosen because it best fit the # of requests/second
    p = Pool(workers, initializer=initialize_worker)
    
    time_init = time()

    # Running Perspective
    add_perspective(dict_c, value_dict)

    # FeedBack at the end
    time_end = time()
    print(f"Time to finish the analysis: {round((time_end-time_init) / 60, 2)}")
