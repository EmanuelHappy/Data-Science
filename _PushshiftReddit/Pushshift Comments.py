'''Import the relevant modules'''

import requests
import json
import csv
import datetime

'''Build Function that builds PushShift URLs'''

def getPushshiftDataComents(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/comment/?title='+str(query)+'&size=500&after='+str(after)+'' \
        '&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

'''Build Function to extract key data points'''

def collectComData(com):
    comData = list()
    body = com['body'].replace(';', '')
    author = com['author']
    com_id = com['id']
    score = com['score']
    parent_id = com['parent_id']
    created = datetime.datetime.fromtimestamp(com['created_utc']) # MGTOW = 1307205635 - 06/04/2011

    comData.append((com_id, body, author, score, parent_id, created))
    comStats[com_id] = comData

def updateSubs_and_Coments_file(sub):
    upload_com_count = 0
    file = f"Comments-Data/{sub}_Comments.csv"
    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file)
        headers = ["ID", "Comment", "Author", "Score", "Parent id", "Publish Date"]
        a.writerow(headers)

        for com in comStats:
            a.writerow(comStats[com][0])
            upload_com_count += 1

        print(str(upload_com_count) + " comments have been uploaded")

'''Where and what data will we be storing?'''

#List of subreddits:
Subreddits = ['MGTOW', 'exredpill', 'RedPillParenting', 'redpillbooks', 'TheRedPill', 'RedPillWomen', 'asktrp',
              'thankTRP', 'becomeaman', 'GEOTRP', 'TRPOffTopic', 'Braincels', 'askanincel', 'BlackPillScience',
              'IncelsWithoutHate', 'ForeverAlone', 'MensRightsLaw', 'MRActivism', 'FeMRA', 'LadyMRAs', 'Masculism',
              'MensRants', 'MRRef', 'FeMRADebates', 'againstmensrights', 'TheBluePill']


'''Run code and loop until all submissions are collected'''

for sub in Subreddits:
    # before and after dates
    before = '1555257518'  # 04/14/2019
    after = '1119484800'  # 06/23/2005 reddit creation
    query = ''  # store all submissions and comments
    comCount = 0
    comStats = {}

    data_com = getPushshiftDataComents(query, after, before, sub)

# Will run until all posts have been gathered
# from the 'after' date up untill before date

#while len(data_com) > 0:
    for coms in data_com:
        collectComData(coms)
        comCount+=1
    # Calls getPushshiftDataComs() with the created date of the las coment
    print(len(data_com))
    print(str(datetime.datetime.fromtimestamp(data_com[-1]['created_utc'])))
    after = data_com[-1]['created_utc']
    data_com = getPushshiftDataComents(query, after, before, sub)

    print(len(data_com))

    '''Check submissions'''

    print(str(len(comStats)) + " Coments have added to list")

    '''Upload to CSV file'''


    updateSubs_and_Coments_file(sub)
