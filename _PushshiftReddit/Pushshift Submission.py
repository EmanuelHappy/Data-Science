import requests
import json
import csv
import datetime

'''Build Function that builds PushShift URLs'''

def getPushshiftDataSubmissions(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=500&after='+str(after)+'' \
        '&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

'''Build Function to extract key data points'''

def collectSubData(subm):
    subData = list() #list to store data points
    title = subm['title'].replace(';', '')
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    numComms = subm['num_comments']
    over_18 = subm['over_18']
    try:
        selftext = subm['selftext'].replace(';', '')
    except KeyError:
        selftext = "NaN"
    try:
        description = subm['description'].replace(';', '')
    except KeyError:
        description = "NaN"

    created = datetime.datetime.fromtimestamp(subm['created_utc']) # reddit creation = 1119484800 06/23/2005

    subData.append((sub_id, title, author, score, numComms, over_18, selftext, description, created))
    subStats[sub_id] = subData

'''Build Function that write the csv'''

def updateSubs__file(sub):
    upload_subm_count = 0
    file = f"Submissions-Data/{sub}_Submissions.csv"

    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file)
        headers = ["Post ID", "Title", "Author", "Score", "No. of Comments", "Over 18", "Selftext", "Description", "Publish Date"]
        a.writerow(headers)

        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_subm_count+=1

        print(str(upload_subm_count) + f" submissions have been uploaded at {sub}.csv")

'''Storing data'''

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
    subCount = 0
    subStats = {}

    data = getPushshiftDataSubmissions(query, after, before, sub)

# Will run until all posts have been gathered
# from the 'after' date up untill before date

# while len(data_com) > 0::
# starting with an small data collections, I omit the loop, so only the first 500 comments will be added

    for submission in data:
        collectSubData(submission)
        subCount+=1

    # Calls getPushshiftDataSubmission() with the created date of the las submission

    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftDataSubmissions(query, after, before, sub)

    '''Check submissions'''

    print(str(len(subStats)) + " submissions have added to list")

    '''Upload to CSV file'''


    updateSubs__file(sub)
