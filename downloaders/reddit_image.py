from .base_downloader import BaseDownloader
from post import Post


class RedditImage(BaseDownloader):
    def __init__(self, post: 'Post', download_dir: str) -> None:
        super().__init__(post, download_dir)

    def download(self):
        return [self._save(self.post.url)]
