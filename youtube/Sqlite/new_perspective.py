__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import json
import argparse
import itertools

from googleapiclient import discovery
from requests import Session
from requests_html import HTMLSession
from multiprocessing import Pool
from time import time, sleep
from sqlitedict import SqliteDict


parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on perspective API scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="perspective_value.sqlite",
                    help="Sqlite DataBase to store the perspective values.")

parser.add_argument("--init", dest="init", type=int, default="0",
                    help="Comment where the analysis begin.")

parser.add_argument("--end", dest="end", type=int, default="1000",
                    help="Comment where the analysis end.")

parser.add_argument("--loop", dest="loop", type=int, default="1",
                    help="Comment where the analysis end.")

args = parser.parse_args()

# Parameters for the perspective api

attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT',
              'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT', 'FLIRTATION']

dict_attributes = {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {},
                   'PROFANITY': {}, 'THREAT': {}, 'SEXUALLY_EXPLICIT': {}, 'FLIRTATION': {}}

data_dict = {'comment': {'text': ''},
             'languages': ['en'],
             'requestedAttributes': dict_attributes}


def initialize_worker():
    """
    Initialize global session for the pools
    :return:
    """
    global session_global
    session_global = HTMLSession()


def process_text(key, text, db):
    """
    Make a perspective request for the text in parallel
    :param text: String that will be analysed by the perspective api
    :return: Dictionary with the request values
    """
    perspective_values = dict()
    data_dict['comment']['text'] = text

    session = session_global
    response = session.post(url=url, json=data_dict)
    value_dict = SqliteDict(db, tablename="value", journal_mode='OFF')

    response_dict = json.loads(response.content)

    for attr in attributes:
        perspective_values[attr] = response_dict['attributeScores'][attr]['summaryScore']['value']

    value_dict[key] = perspective_values
    value_dict.commit()
    value_dict.close()
    session.cookies.clear()


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
    workers = 500  # The number 20 was chosen because it best fit the # of requests/second
    p = Pool(workers, initializer=initialize_worker)

    time_iter = time()
    print("bla", args.init, args.end)
    to_request = [(k, v["text"], args.dst) for k, v in itertools.islice(dict_c.items(), args.init, args.end)]
    time_end = time()
    dif = (args.end - args.init)//args.loop
    print(f"Time to iter: {round((time_end - time_iter) / 60, 2)}")
    for i in range(args.loop):
        time_init = time()
        p.starmap(process_text, to_request[i*dif:(i+1)*dif])
        time_end = time()
        dt = time_end-time_init
        print(f"Time to run the {i} loop is {round(dt/60, 2)}")
        if i != args.loop -1:
            sleep(100-dt)

    # Running Perspective
    # add_perspective(to_request, dict_c, value_dict, p)
    #
    # # FeedBack at the end
    time_end = time()
    print(f"Time to finish the analysis: {round((time_end - time_init) / 60, 2)}")
    
