from __future__ import annotations

import logging
import os
import re

import pandas as pd
import praw

from file_utils import get_id_and_keys


def update_new_posts(api_keys: tuple[str, str], subreddit: str | tuple[str, ...],
                     database_path: str = 'databases/reddit_database.csv', user_agent: str = 'My API/0.0.1',
                     limit: int = 20) -> str:
    CLIENT_ID, CLIENT_SECRET = api_keys
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=user_agent)
    logging.info(f'Connected to Reddit API')
    if isinstance(subreddit, tuple):
        subreddit = [f'{each}+' if i != len(subreddit) - 1 else each for i, each in enumerate(subreddit)]
    posts = reddit.subreddit(subreddit).hot(limit=limit)
    logging.info(f'Retrieved {limit} posts from {subreddit}')
    database = pd.DataFrame(
        columns=['title', 'url', 'subreddit', 'score', 'created_utc', 'id', 'video', 'audio']) if not os.path.exists(
        database_path) else pd.read_csv(database_path)
    for post in posts:
        if post.id not in database['id'].values and post.is_video:
            video_url = post.media['reddit_video']['fallback_url']
            database = database.append({
                'title': post.title, 'url': post.url, 'subreddit': post.subreddit.display_name, 'score': post.score,
                'created_utc': post.created_utc, 'id': post.id, 'video': video_url,
                'audio': re.sub(r'DASH_\d+.mp4', 'DASH_audio.mp4', video_url)}, ignore_index=True)
            logging.info(f'Added {post.title} to database')
    database.to_csv(database_path, index=False)
    logging.info(f'Database updated')

    return database_path


if __name__ == '__main__':
    database = 'databases/abrupt_chaos.csv'
    test_api_keys = get_id_and_keys('credentials/reddit_api_keys.txt')
    reddit = praw.Reddit(client_id=test_api_keys[0], client_secret=test_api_keys[1], user_agent='My API/0.0.1')
    update_new_posts(test_api_keys, 'abruptchaos', database_path=database, limit=20)
