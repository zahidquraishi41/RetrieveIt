from post import Post
from typing import List
from pathvalidate import sanitize_filename
import requests
import re
import os
import time


class BaseDownloader:
    def __init__(self, post: 'Post', download_dir: str) -> None:
        self.download_dir = download_dir
        self.post = post

    def download(self) -> List[str]:
        # returns the filepath where media is downloaded; filename and extension is generated from submission.
        raise NotImplementedError()

    def _generate_filepath(self, url: str) -> str:
        '''Generate a unique filepath based on the submission title. 
        It removes any invalid characters for a filename, and prefixes the resulting
        sanitized title with a timestamp to create a unique filename. Url is used for 
        extracting the media type.'''
        # Sanitizing filename
        filename = sanitize_filename(
            self.post.title,
            replacement_text=' ',
            max_len=180
        )
        filename = re.sub(r'\s+', ' ', filename).strip()

        # Extracting extension
        extension = url.rsplit('.')[-1].split('?')[0].lower()
        extension = extension if extension and len(extension) < 5\
            else 'unknown'
        filename += f'.{extension}'

        # Generating unique timestamp
        while True:
            timestamp = str(int(time.time()))
            filepath = os.path.join(
                self.download_dir,
                timestamp + ' - ' + filename
            )
            if not os.path.exists(filepath):
                break
        return filepath

    def _save(self, url: str) -> str:
        '''Saves media from the specified URL to the local disk with a unique filename.
        Returns:
            filepath of downloaded content.
        '''
        os.makedirs(self.download_dir, exist_ok=True)
        filepath = self._generate_filepath(url)
        response = requests.get(url)
        if not response.ok:
            raise Exception('Failed to connect to internet.')
        try:
            with open(filepath, 'wb') as f:
                f.write(response.content)
        except:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise
        return filepath
