
## redditstream-cli 

redditstream-cli is a command line tool/interface for live streaming reddit comments from any subreddit. It updates automatically, pulling the latest comments and printing them into a nice columnar format for you to view. 

It is written in Python, utilizing the PRAW Reddit API.

1. First, sign up [here](https://www.reddit.com/prefs/apps/) for the PRAW API access to reddit. 

2. Create a file called credentials.json in the redditstream-cli/code directory. The credentials.json file should be formatted like this:

```json
{
 "client_id":"l-suwe93841bPg",
 "client_secret":"EndSlPnoEJtEqOqo",
 "password":"xxxxx",
 "user_agent":"testscript",
 "username":"RedditUsername"
}

```
3. Lastly, change to the directory of the .py script and run 

`python redditstream-cli.py -s soccer`

This will start a live comment streaming session from [reddit.com/r/soccer](http://reddit.com/r/soccer)

Here is an example of three different redditstream-cli sessions running, serving the latest comments from r/politics, r/soccer, and r/technology. 

![Alt Test](https://github.com/claytonblythe/redditstream-cli/blob/master/figures/screenshot.png)

Here is a demo of how to run it, and what it looks like in action! 
[![demo](https://asciinema.org/a/JZhJWeNvq1bTI8tG4VbaYPfJS.png)](https://asciinema.org/a/JZhJWeNvq1bTI8tG4VbaYPfJS?autoplay=1) 


If you want to help out with this project or have suggestions/requests for features let me know!

I eventually want to make it more interactive, to allow you to change the subreddit or filter out certain submissions. So far I would consider this the alpha version. 

Hope you like it!
 
-Clayton Blythe
claytondblythe@gmail.com
