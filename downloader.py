from downloaders.reddit_image import RedditImage
from downloaders.reddit_video import RedditVideo
from downloaders.reddit_gallery import RedditGallery
from post import Post, MediaType
import os
import re


class Downloader:
    def __init__(self, download_dir: str) -> None:
        self._download_dir = download_dir
        self._supported_domain = ('i.redd.it', 'v.redd.it', 'reddit.com')

    def download(self, post: 'Post'):
        assert re.search('|'.join(self._supported_domain), post.domain), \
            f"ID: {post.id} has unsupported domain."

        nsfw = '_NSFW' if post.nsfw else ''
        download_dir = os.path.join(
            self._download_dir,
            f'Videos{nsfw}' if post.media_type == MediaType.VIDEO else f'Images{nsfw}',
            post.subreddit
        )

        if post.media_type == MediaType.IMAGE:
            RedditImage(post, download_dir).download()
        elif post.media_type == MediaType.GALLERY:
            RedditGallery(post, download_dir).download()
        elif post.media_type == MediaType.VIDEO:
            RedditVideo(post, download_dir).download()
