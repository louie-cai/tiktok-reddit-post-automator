import file_utils
import video_production
import reddit_utils
import selenium_utils
import pandas as pd
import os
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s %(levelname)s] %(message)s')
    api_keys = file_utils.get_id_and_keys('credentials/reddit_api_keys.txt')
    database = 'databases/abrupt_chaos.csv'
    reddit_utils.update_new_posts(api_keys, 'abruptchaos', database_path=database, limit=20)
    data = pd.read_csv(database)
    clips_path = 'clips'
    uploaded_video_set = set(open('clips/uploaded_videos.txt', 'r').read().splitlines())
    for _, row in data.iterrows():
        if os.path.exists(os.path.join(clips_path, f'{row["id"]}.mp4')):
            continue
        file_utils.download_video_and_audio(row['video'], row['audio'], row['id'], clips_path)
        video_production.combine_video_audio(os.path.join(clips_path, f'{row["id"]}_video.mp4'),
            os.path.join(clips_path, f'{row["id"]}_audio.mp4'), row['id'], clips_path)
        if row['id'] not in uploaded_video_set:
            selenium_utils.upload_video('./chromedriver', os.path.join(clips_path, f'{row["id"]}.mp4'), row['url'])
            with open('clips/uploaded_videos.txt', 'a+') as file:
                file.write(f'{row["id"]}\n')
        logging.info(f'Video uploaded for {row["id"]}')
        logging.info(f'Sleeping for 60 seconds')
        time.sleep(60)
