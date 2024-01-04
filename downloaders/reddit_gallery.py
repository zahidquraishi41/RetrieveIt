from .base_downloader import BaseDownloader
from post import Post


class RedditGallery(BaseDownloader):
    def __init__(self, post: 'Post', download_dir: str) -> None:
        super().__init__(post, download_dir)

    def download(self):
        base_url = 'https://i.redd.it/'
        urls = []
        for media in self.post.gallery_data['items']:
            media_id = media['media_id']
            ext = self.post.media_metadata[media_id]['m'].split('/')[1]
            url = base_url + media_id + '.' + ext
            urls.append(url)

        return [self._save(url) for url in urls]
