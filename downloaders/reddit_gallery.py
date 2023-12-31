from .base_downloader import BaseDownloader
from post import Post


class RedditGallery(BaseDownloader):
    def __init__(self, post: 'Post', download_dir: str) -> None:
        super().__init__(post, download_dir)

    def download(self):
        base_url = 'https://i.redd.it/'
        urls = []
        for k, v in self.post.media_metadata.items():
            ext = v['m'].split('/')[1]
            url = base_url + k + '.' + ext
            urls.append(url)

        return [self._save(url) for url in urls]
