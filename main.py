import praw
import secrets
import datetime
from langdetect import detect

def driver_login():
    client = praw.Reddit(username = secrets.username,
                         password = secrets.password,
                         client_id = secrets.client_id,
                         client_secret = secrets.secret,
                         user_agent = "dt user analyzer v0.2")
    return client

def run_bot(driver):
    print('[*] Starting Search')
    for comment in driver.subreddit('privacy').comments(limit=25):
        print("\n" + comment.body)

def user_top_comments(user, max):
    print('[*] Retrieving top ' + str(max) + ' comments')
    comments_top = user.comments.top(limit=max)
    for comment in comments_top:
        print("\n--------------------------------------------")
        print(comment.body)
        get_date(comment)
        print("--------------------------------------------")

def get_date(item):
    time = item.created
    print("Posted On: " + str(datetime.date.fromtimestamp(time)) +
          " at: " + str(datetime.datetime.fromtimestamp(time))[-8:])

    #print(datetime.datetime.fromtimestamp(time))

def main(driver, target):
    user = driver.redditor(target)
    print("[*] Getting /u/" + target + " account data")
    print("[+] Karma: " + str(user.comment_karma + user.link_karma)) # possibly split this into 2
    print("[+] Lang: " + detect(str((user.comments.top(limit=1)))))
    print("[+] Account Created: ")
    user_top_comments(user, 10)

driver = driver_login()
main(driver, 'xraptorz')