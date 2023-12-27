from post import Post
from .base_downloader import BaseDownloader
import requests
from xml.dom import minidom
from moviepy.editor import AudioFileClip, VideoFileClip
import os


class RedditVideo(BaseDownloader):
    def __init__(self, post: 'Post', download_dir: str) -> None:
        super().__init__(post, download_dir)

    def _parse_mpd(self) -> 'minidom.Document':
        '''The mpd file contains list of video and audio quality available.'''
        dash_url = self.post.media['reddit_video']['dash_url']
        mpd = requests.get(dash_url).text
        return minidom.parseString(mpd)

    def download(self):
        dom = self._parse_mpd()
        adaptation_set = dom.getElementsByTagName('AdaptationSet')

        # downloading video
        base_url = adaptation_set[0].getElementsByTagName('BaseURL')[0]\
            .firstChild.nodeValue
        video_url = self.post.url + '/' + base_url
        video_path = self._save(video_url)

        if len(adaptation_set) == 1:
            print('Warning: No audio found.')
            return video_path

        # downloading audio
        base_url = adaptation_set[1].getElementsByTagName('BaseURL')[0]\
            .firstChild.nodeValue
        audio_url = self.post.url + '/' + base_url
        audio_path = self._save(audio_url)

        # merging video and audio
        try:
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            video_clip = video_clip.set_audio(audio_clip)
            merged_path = self._generate_filepath(video_url)
            video_clip.write_videofile(
                merged_path,
                codec="libx264",
                audio_codec="aac",
                logger=None
            )
        except:
            if os.path.exists(merged_path):
                os.remove(merged_path)
            raise
        finally:
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
            if 'video_clip' in locals() and video_clip:
                video_clip.close()
            if 'audio_clip' in locals() and audio_clip:
                audio_clip.close()
        return merged_path
