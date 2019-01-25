## Reddit Post Analyzer 

#### Installation
⚠ API keys and Python2.7 or are newer are required.

To generate API keys, create a 'script' at: https://www.reddit.com/prefs/apps/

Next, create a file named _secrets.py_ in the same folder as reddit_analzer.py.  The file contents should appear as followed:
```
username  = 'your account username'
password  = 'your account password'
client_id = 'generated client id'
secret    = 'generated secret key'
```

Finally, install requirements using:
```
pip install -r requirements.txt
```

#### Usage
```
usage: reddit_analyzer.py -n <screen_name> [options]
options:
-a --all              - gather dataset of both comments and posts
-p --posts            - gather dataset of user's submitted posts
-c --comments         - gather dataset of user's comments
-nc --no-color        - turns off colored output
-l --limit            - set a max amount of posts collected (default=1000)
--new                 - gather dataset from posts sorted by new (default=top posts)
-utc --utc-offset     - offset time information to allign with timezone(+- UTC)
-v --verbose          - allow verbose analysis of collected data
-vn --verbose_num     - use in conjunction with -v to limit the amount of data returned (default=5)

Examples: 
reddit_analyzer.py -n mctesty
reddit_analyzer.py -n mctesty -a --new -l 100
reddit_analyzer.py -n mctesty -utc -5 -nc -p
```

#### Example Output
![alt text](https://i.imgur.com/mX9dvc5.png)