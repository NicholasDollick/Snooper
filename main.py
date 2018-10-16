import praw
import secrets
import datetime

def driver_login():
    client = praw.Reddit(username = secrets.username,
                         password = secrets.password,
                         client_id = secrets.client_id,
                         client_secret = secrets.secret,
                         user_agent = "dt user analyzer v0.1")
    print('[+] client logged in')
    return client

def run_bot(driver):
    print('[*] Starting Search')
    for comment in driver.subreddit('privacy').comments(limit=25):
        print("\n" + comment.body)

def user_top_comments(driver, target, max):
    print("[+] Target: " + target)
    print('[*] Starting Search')
    user = driver.redditor(target)
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

driver = driver_login()
user_top_comments(driver, 'xraptorz', 10)