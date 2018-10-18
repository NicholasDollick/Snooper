# Usage:
# python reddit_analyzer.py -n screen_name

import argparse
import praw
import secrets
import datetime
from langdetect import detect
from ascii_graph import Pyasciigraph
from ascii_graph.colors import Gre, Yel, Red
from ascii_graph.colordata import hcolor
import numpy as np
from tqdm import tqdm
import sys

parser = argparse.ArgumentParser(description='Simple Reddit Profile Analyzer v.06',
                                 usage='reddit_analyzer.py -n <screen_name> [options]')

parser.add_argument('-n', '--name', required=True, metavar="screen_name",
                    help='target screen_name')

parser.add_argument('-a', '--all', action='store_true', help='Combine and analyze post + comment data')

parser.add_argument('-l', '--limit', metavar='N', type=int, default=1000,
                    help='limit the number of posts to retrieve (default=1000)')

parser.add_argument('-c', '--comments', action='store_true', help='analyze only user comments')

parser.add_argument('-p', '--posts', action='store_true', help='analyze only user submissions')

parser.add_argument('-e', '--export', metavar='path/to/file', type=str, help='exports results to file')

parser.add_argument('-nc', '--no-color', action='store_true', help='disables colored output')

parser.add_argument('-utc', '--utc-offset', type=int, help='manually apply a timezone offset (from UTC)')

parser.add_argument('-v', '--verbose', action='store_true', help='allow verbose analysis of collected data')

parser.add_argument('--new', action='store_true' ,help='')

parser.add_argument('--debug', action='store_true')

args = parser.parse_args()

def driver_login():
    client = praw.Reddit(username = secrets.username,
                         password = secrets.password,
                         client_id = secrets.client_id,
                         client_secret = secrets.secret,
                         user_agent = "dt user analyzer v0.6")
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

def analyze_by_day(data, chart_title): # perhaps consider also account for posts by day
    dataset = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0,
               'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
    for item in data:
        dataset[int_to_day(get_day(item))] += 1

    print_graph(dataset, chart_title)

def analyze_by_hour(data, chart_title):
    dataset = {'00:00':0, '01:00':0, '02:00':0, '03:00':0, '04:00':0, '05:00':0, '06:00':0, '07:00':0, '08:00':0,
               '09:00':0, '10:00':0, '11:00':0, '12:00':0, '13:00':0, '14:00':0, '15:00':0, '16:00':0, '17:00':0,
               '18:00':0, '19:00':0, '20:00':0, '21:00':0, '22:00':0, '23:00':0, '24:00':0
               }
    for item in data:
        time = item.created
        dataset[str(datetime.datetime.fromtimestamp(time))[11:13] + ":00"] += 1
    print_graph(dataset, chart_title)


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


    if(not args.no_color):
        thresholds = {
            int(mean): Gre, int(mean * 2): Yel, int(mean * 3): Red,
        }

        data = hcolor(chart, thresholds)
    else:
        data = chart

    for line in graph.graph(title, data):
        print(line)


def main(driver, target):
    total_data = []
    graph_of = ""
    user = driver.redditor(target)
    print("[*] Getting /u/" + target + "'s account data")

    if(args.all):
        if(args.new):
            posts = user.submissions.new(limit=args.limit)
            comments = user.comments.new(limit=args.limit)
        else:
            posts = user.submissions.top(limit=args.limit)
            comments = user.comments.top(limit=args.limit)

        total_data = list(posts) + list(comments)
        graph_of = 'Total '

    elif(args.comments):
        if(args.new):
            total_data = list(user.comments.new(limit=args.limit))
        else:
            total_data = list(user.comments.top(limit=args.limit))
        graph_of = 'Comment '

    elif(args.posts):
        if(args.new):
            total_data = list(user.submissions.new(limit=args.limit))
        else:
            total_data = list(user.submissions.top(limit=args.limit))
        graph_of = 'Submission '

    else:
        if(args.new):
            total_data = list(user.comments.new(limit=args.limit))
        else:
            total_data = list(user.comments.top(limit=args.limit))
        graph_of = 'Comment '

    if(args.debug):
        if(args.utc_offset != None):
            print((args.utc_offset))
        else:
            print("uwu")
        sys.exit(0)

    print("[+] Karma: " + str(user.comment_karma + user.link_karma) + " (Comment: "
          + str(user.comment_karma) + " Link: " + str(user.link_karma) + ")") # possibly split this into 2
    print("[+] Lang: " + detect(str((user.comments.top(limit=1)))))
    print("[+] Account Created: " + str(datetime.datetime.fromtimestamp(user.created_utc)))
    analyze_by_hour(total_data, graph_of + 'activity distribution (per hour)') # this string needs to be decided by args
    analyze_by_day(total_data, graph_of + 'activity distribution (per day)')



try:
    driver = driver_login()
    main(driver, args.name)
except Exception as e:
    print(e)

