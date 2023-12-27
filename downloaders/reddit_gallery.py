from .base_downloader import BaseDownloader
from post import Post


class RedditGallery(BaseDownloader):
    def __init__(self, post: 'Post', download_dir: str) -> None:
        super().__init__(post, download_dir)

    def download(self):
        base_url = 'https://i.redd.it/'
        ids = list(self.post.media_metadata.keys())
        ext = self.post.media_metadata[ids[0]]['m'].split('/')[1]

        urls = [base_url + id + '.' + ext for id in ids]
        for url in urls:
            self._save(url)
