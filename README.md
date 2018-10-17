## Reddit Post Analyzer 

####Installation
⚠ API keys and Python2.7 or are newer are required.

To generate API keys, create a 'script' at: https://www.reddit.com/prefs/apps/

Next, create a file named _secrets.py_ in the same folder as reddit_analzer.py.  The file contents should appear as followed:
```
username  = 'your account username'
password  = 'your account password'
client_id = '### generated client id ###'
secret    = '### generated secret key ###'
```

Finally, install requirements using:
```
pip install -r requirements.txt
```

####Usage
```
usage: tweets_analyzer.py -n <screen_name> [options]
```