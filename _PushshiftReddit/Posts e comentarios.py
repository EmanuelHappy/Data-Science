'''Import the relevant modules'''

import requests
import json
import csv
import datetime

'''Build Function that builds PushShift URLs'''

def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'' \
        '&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def getPushshiftDataComents(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/comment/?title='+str(query)+'&size=1000&after='+str(after)+'' \
        '&before='+str(before)+'&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

'''Build Function to extract key data points'''

def collectSubData(subm):
    subData = list() #list to store data points
    title = subm['title']
    sub_id = subm['id']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) # MGTOW = 1442108090

    subData.append((sub_id, title, created))
    subStats[sub_id] = subData

def collectComData(com):
    comData = list()
    body = com['body']
    com_id = com['id']
    created = datetime.datetime.fromtimestamp(com['created_utc']) # MGTOW = 1442108090

    comData.append((com_id, body, created))
    comStats[com_id] = comData


'''Where and what data will we be storing?'''

#Subreddit to query
sub='MGTOW'
#before and after dates
before = '1354694719' # 04/08/2019
after = '1307205635' # 06/04/2011
query = '' # submissions with "Screenshot" in the title -> let's retire
subCount = 0
subStats = {}
comCount = 0
comStats = {}

'''Run code and loop until all submissions are collected'''
'''Run code and loop until all comments are collected'''

data = getPushshiftData(query, after, before, sub)
data_com = getPushshiftDataComents(query, after, before, sub)

# Will run until all posts have been gathered
# from the 'after' date up untill before date
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    # Calls getPushshiftData() with the created date of the las submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)

while len(data_com) > 0:
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

print(str(len(subStats)) + " submissions have added to list")
print(str(len(comStats)) + " Coments have added to list")
'''print("1st entry is:")
print(list(subStats.values())[0][0][1] + " created: " + str(list(subStats.values())[0][0][5]))
print("Last entry is:")
print(list(subStats.values())[-1][0][1] + " created: " + str(list(subStats.values())[-1][0][5]))'''

'''Upload to CSV file'''

def updateSubs_and_Coments_file():
    upload_count = 0
    upload_com_count = 0
    location = "C:\\Users\\emanu\\programacao\\jupiter\\Trabalho Prático Semana1\\"
    print("input filename of submission file, plead add .csv")
    filename = input()
    file = location + filename

    with open(file, 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file)
        headers = [" Title and Coments"]
        a.writerow(headers)

        for sub in subStats:
            a.writerow(subStats[sub][0][1:2])
            upload_count+=1
        a.writerow('Here start the comments')

        for com in comStats:
            a.writerow(comStats[com][0][1:2])
            upload_com_count += 1

        print(str(upload_count) + " submissions have been uploaded")
        print(str(upload_com_count) + " comments have been uploaded")

updateSubs_and_Coments_file()
