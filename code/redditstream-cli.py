import praw
import textwrap
import argparse
import json
import os
import sqlite3

"""This is a script to live stream reddit comments from any subreddit, and store the results in a sqlite database.
    Script can be run like "python redditstream-cli.py -s soccer" to initialize and start streaming/storing. The 
    possibilities here are really interesting, you could do things like sentiment analysis or use the data for making 
    a chat bot that talks in a certain subreddit's style. 
    Author: Clayton Blythe Email: claytondblythe@gmail.com """

def get_args():
    """This function parses and return arguments passed in, classic argparse"""
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

def authenticate():
    with open('credentials.json') as creds:

        credentials = json.load(creds)

    reddit = praw.Reddit(client_id=credentials['client_id'],
                        client_secret=credentials['client_secret'],
                         password=credentials['password'],
                         user_agent=credentials['user_agent'],
                         username=credentials['username'])
    reddit.read_only = True
    return(reddit)

def check_database_exists(subreddit):
    # Create the database subreddit.db if it does not exist
    # Here the UNIQUE constraint will maintain we don't insert duplicate
    # comment_id's into the subreddit table in that database
    if not os.path.exists('../data/{}.db'.format(subreddit)):
        conn = sqlite3.connect('../data/{}.db'.format(subreddit))
        c = conn.cursor()
        c.execute("""CREATE TABLE {}
                         (user, time, comment, comment_id, post_title, post_id, url, UNIQUE(comment_id))""".format(
            subreddit))
        conn.commit()
        conn.close()


def print_db_size(subreddit, cursor):
    # Find how many rows are in the database before closing
    cursor.execute("SELECT COUNT (*) FROM {}".format(subreddit))
    rowcount = cursor.fetchone()[0]
    print('Number of comments in {} database: {}\n'.format(subreddit, rowcount))


def stream_and_insert(subreddit, cursor):
    print("\nBeginning comment stream for r/{}\n".format(subreddit.display_name))
    print('-----------------------------------------------------------')
    while True:
        try:
            for comment in subreddit.stream.comments(pause_after=0):
                if comment is None:
                    pass
                else:
                    user, time, body = comment.author.name, comment.created_utc, "\n".join(
                        textwrap.wrap(textwrap.dedent(comment.body).strip(), width=60))
                    comment_id, post_title, post_id, url = comment.id, comment.link_title, comment.link_id, comment.link_url
                    #     if post_id == 't3_7b0eae':
                    print('u/' + user + ":\n" + body)
                    print('-----------------------------------------------------------')
                    cursor.execute("""INSERT OR REPLACE INTO {} VALUES (?,?,?,?,?,?,?);""".format(subreddit),
                              (user, time, body, comment_id, post_title, post_id, url))
        except KeyboardInterrupt:
            print('\nBreaking loop and saving database')
            break


def main():
    """Main script to get command line arguments, start streaming reddit comments, and store in sqlite database."""
    a_subreddit = get_args()
    reddit = authenticate()
    subreddit = reddit.subreddit(a_subreddit)
    check_database_exists(subreddit)
    conn = sqlite3.connect('../data/{}.db'.format(subreddit))
    c = conn.cursor()
    stream_and_insert(subreddit=subreddit, cursor=c)
    print_db_size(subreddit=subreddit, cursor=c)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()