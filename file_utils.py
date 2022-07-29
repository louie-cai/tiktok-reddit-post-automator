import urllib.request
import os
import logging


def get_id_and_keys(path: str) -> tuple[str, str]:
    """
    Get the username and password from the file at the given path.
    :param path: path to the file containing the API keys
    :return: the username and password
    """
    with open(path, 'r') as f:
        keys = f.read().splitlines()
        logging.info(f'API keys read from {path}')
        return keys[0], keys[1]


def download_video_and_audio(video_url: str, audio_url: str, post_id: str, path: str = 'clips') -> tuple[str, str]:
    logging.info(f'Downloading video and audio for {post_id}')
    video_path = os.path.join(path, f'{post_id}_video.mp4')
    audio_path = os.path.join(path, f'{post_id}_audio.mp4')
    urllib.request.urlretrieve(video_url, video_path)
    urllib.request.urlretrieve(audio_url, audio_path)
    logging.info(f'Video and audio downloaded for {post_id}')
    return video_path, audio_path


if __name__ == '__main__':
    print(f'Reddit API Keys: {get_id_and_keys("credentials/reddit_api_keys.txt")}')
