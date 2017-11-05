import praw
import textwrap
import argparse
import json

def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Command line interface for streaming latest comments from a subreddit')
    # Add arguments
    parser.add_argument(
        '-s', '--subreddit', type=str, help='Subreddit name', default='soccer')
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    a_subreddit = args.subreddit
    # Return all variable values
    return a_subreddit


with open('credentials.json') as creds:
    credentials = json.load(creds)

reddit = praw.Reddit(client_id=credentials['client_id'],
                    client_secret=credentials['client_secret'],
                     password=credentials['password'],
                     user_agent=credentials['user_agent'],
                     username=credentials['username'])
reddit.read_only = True

a_subreddit = get_args()
subreddit = reddit.subreddit(a_subreddit)
print("Beginning comment stream for r/{}".format(subreddit.display_name))
print('-----------------------------------------------------------')
for comment in subreddit.stream.comments(pause_after=0):
    if comment is None:
        pass
    else:
        user, time, body = comment.author.name, comment.created_utc, "\n".join(textwrap.wrap(textwrap.dedent(comment.body).strip(), width=60))
        comment_id, post_title, post_id, url = comment.id, comment.link_title, comment.link_id, comment.link_url
        print('u/' + user + ":\n" + body)
        print('-----------------------------------------------------------')
