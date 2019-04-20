import csv

fin = open('Subreddits')

file = "subreddits.csv"
with open(file, 'w', newline='', encoding='utf-8') as file:
    a = csv.writer(file)
    header = ["Subreddits"]
    a.writerow(header)

    for subreddit in fin:
        a.writerow([subreddit])
