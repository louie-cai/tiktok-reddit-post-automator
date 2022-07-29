import logging
import os

import moviepy.editor as mp


def combine_video_audio(video_path: str, audio_path: str, id: str, output_path: str = 'clips') -> str:
    logging.info(f'Combining video and audio for {id}')
    video = mp.VideoFileClip(video_path)
    audio = mp.AudioFileClip(audio_path)
    video.audio = audio
    video.write_videofile(os.path.join(output_path, f'{id}.mp4'))
    logging.info(f'Video and audio combined for {id}')
    return output_path
