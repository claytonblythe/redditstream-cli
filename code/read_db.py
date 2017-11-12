import sqlite3
import pandas as pd
import argparse

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

def main():
    subreddit = get_args()
    conn = sqlite3.connect('../data/{}.db'.format(subreddit))
    c = conn.cursor()
    c.execute("SELECT COUNT (*) FROM {}".format(subreddit))
    rowcount = c.fetchone()[0]
    print('\nNumber of comments in {} database: {}\n'.format(subreddit, rowcount))
    df = pd.read_sql_query('SELECT * FROM {}'.format(subreddit), con=conn)
    print()
    print(df[['user', 'comment']])
    conn.close()

if __name__ == "__main__":
    main()