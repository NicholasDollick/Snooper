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
                         user_agent = "dt user analyzer v0.2")
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
    #print(datetime.datetime.fromtimestamp(time))

def get_day(item):
    time = item.created
    return datetime.datetime.fromtimestamp(time).weekday()

def int_to_day(day):
    test = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
    return test[day]

def analyze_by_day(user):
    graph = Pyasciigraph(
        separator_length=4,
        multivalue=False,
        human_readable='si',
    )
    dataset = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0,
               'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
    chart = []
    comments_top = user.comments.top(limit=100)
    comments_top = list(comments_top)

    for comment in tqdm((comments_top), desc='Progress', total=len(comments_top)): # this doesnt do much for some reason
        dataset[int_to_day(get_day(comment))] += 1

    keys = sorted(dataset.keys())
    mean = np.mean(list(dataset.values()))
    #median = np.median(list(dataset.values()))

    for key in keys:
        chart.append((key, dataset[key]))

    thresholds = {
        int(mean): Gre, int(mean * 2): Yel, int(mean * 3): Red,
    }

    data = hcolor(chart, thresholds)

    for line in graph.graph('Comment activity distribution (per day)', data):
        print(line)

def main(driver, target):
    user = driver.redditor(target)
    print("[*] Getting /u/" + target + " account data")
    print("[+] Karma: " + str(user.comment_karma + user.link_karma) + " (Comment: "
          + str(user.comment_karma) + " Link: " + str(user.link_karma) + ")") # possibly split this into 2
    print("[+] Lang: " + detect(str((user.comments.top(limit=1)))))
    print("[+] Account Created: " + str(datetime.datetime.fromtimestamp(user.created_utc)))
    #user_top_comments(user, 10)
    analyze_by_day(user)

driver = driver_login()
main(driver, 'fiomonstercat')