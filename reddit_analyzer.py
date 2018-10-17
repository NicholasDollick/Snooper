# Usage:
# python reddit_analyzer.py -n screen_name

import praw
import secrets
import datetime
from langdetect import detect
from ascii_graph import Pyasciigraph
from ascii_graph.colors import Gre, Yel, Red
from ascii_graph.colordata import hcolor
import numpy as np
from tqdm import tqdm

def driver_login():
    client = praw.Reddit(username = secrets.username,
                         password = secrets.password,
                         client_id = secrets.client_id,
                         client_secret = secrets.secret,
                         user_agent = "dt user analyzer v0.3")
    return client

def run_bot(driver):
    print('[*] Starting Search')
    for comment in driver.subreddit('edm').comments(limit=25):
        print("\n" + comment.body)

def user_top_comments(user, max):
    print('[*] Retrieving top ' + str(max) + ' comments')
    comments_top = user.comments.top(limit=max)
    for comment in comments_top:
        print("\n--------------------------------------------")
        print(comment.body)
        get_day(comment)
        print("--------------------------------------------")

def get_date(item):
    time = item.created
    print("Posted On: " + str(datetime.date.fromtimestamp(time)) +
          " at: " + str(datetime.datetime.fromtimestamp(time))[-8:])

def get_day(item):
    time = item.created
    return datetime.datetime.fromtimestamp(time).weekday()

def int_to_day(day):
    test = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
    return test[day]

def analyze_by_day(user): # perhaps consider also account for posts by day
    dataset = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0,
               'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
    comments_top = user.comments.top(limit=100)

    for comment in comments_top:
        dataset[int_to_day(get_day(comment))] += 1

    print_graph(dataset, 'Comment activity distribution (per day)')

def analyze_by_hour(user):
    dataset = {'00:00':0, '01:00':0, '02:00':0, '03:00':0, '04:00':0, '05:00':0, '06:00':0, '07:00':0, '08:00':0,
               '09:00':0, '10:00':0, '11:00':0, '12:00':0, '13:00':0, '14:00':0, '15:00':0, '16:00':0, '17:00':0,
               '18:00':0, '19:00':0, '20:00':0, '21:00':0, '22:00':0, '23:00':0, '24:00':0
               }
    comments_top = user.comments.top(limit=100)
    for comment in comments_top:
        time = comment.created
        dataset[str(datetime.datetime.fromtimestamp(time))[11:13] + ":00"] += 1
    print_graph(dataset, 'Comment activity distribution (per hour)')


def print_graph(dataset, title):
    graph = Pyasciigraph(
        separator_length=4,
        multivalue=False,
        human_readable='si',
    )
    chart = []
    keys = sorted(dataset.keys())
    mean = np.mean(list(dataset.values()))
    #median = np.median(list(dataset.values()))

    for key in keys:
        chart.append((key, dataset[key]))

    thresholds = {
        int(mean): Gre, int(mean * 2): Yel, int(mean * 3): Red,
    }

    data = hcolor(chart, thresholds)

    for line in graph.graph(title, data):
        print(line)


def main(driver, target):
    user = driver.redditor(target)
    print("[*] Getting /u/" + target + " account data")
    print("[+] Karma: " + str(user.comment_karma + user.link_karma) + " (Comment: "
          + str(user.comment_karma) + " Link: " + str(user.link_karma) + ")") # possibly split this into 2
    print("[+] Lang: " + detect(str((user.comments.top(limit=1)))))
    print("[+] Account Created: " + str(datetime.datetime.fromtimestamp(user.created_utc)))
    #user_top_comments(user, 10)
    analyze_by_hour(user)
    analyze_by_day(user)

driver = driver_login()
main(driver, 'fiomonstercat')