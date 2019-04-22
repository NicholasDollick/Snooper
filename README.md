<p align="center">
    <img src="https://i.imgur.com/2MFVX6h.png" alt="logo" width="500"/>
</p>
<p align="center">
    <strong><i>Reddit Post Analyzer</i></strong>
</p>

#### Installation
⚠ API keys and Python2.7 or are newer are required.

To generate API keys, create a 'script' at: https://www.reddit.com/prefs/apps/

Next, create a file named _secrets.py_ in the same folder as snooper.py.  The file contents should appear as followed:
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
usage: snooper.py -n <screen_name> [options]
options:
-h --help             - show this help message and exit
-a --all              - gather dataset of both comments and posts
-p --posts            - gather dataset of user's submitted posts
-c --comments         - gather dataset of user's comments
-nc --no-color        - turns off colored output
-l --limit            - set a max amount of posts collected (default=1000)
--new                 - gather dataset from posts sorted by new (default=top posts)
-utc --utc-offset     - offset time information to allign with timezone(+- UTC)
-v --verbose          - allow verbose analysis of collected data
-vn --verbose_num     - use in conjunction with -v to limit the amount of data returned (default=5)
--get                 - collect all comments and posts from supplied subreddit
-ng --no-graph        - disable printing of graph analyzation

Examples: 
snooper.py -n mctesty
snooper.py -n mctesty -a --new -l 100
snooper.py -n mctesty -utc -5 -nc -p
```

#### Example Output
![](https://i.imgur.com/mX9dvc5.png)