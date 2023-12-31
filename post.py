from praw.models.reddit.submission import Submission
from enum import Enum
import re


class MediaType(Enum):
    IMAGE = 0
    GALLERY = 1
    VIDEO = 2
    COMMENT = 3
    UNKNOWN = 9


class Post:
    def __init__(self, submission: Submission) -> None:
        self.id = getattr(submission, 'id', '')
        self.title = getattr(submission, 'title', '')
        self.url = getattr(submission, 'url', '')
        self.domain = getattr(submission, 'domain', '')
        self.upvotes = getattr(submission, 'score', 0)
        self.created_utc = int(submission.created_utc)
        self.upvotes = getattr(submission, 'score', 0)
        self.media_metadata = getattr(submission, 'media_metadata', {})
        self.gallery_data = getattr(submission, 'gallery_data', {})
        self.media = getattr(submission, 'media', {})
        self.subreddit = getattr(
            getattr(submission, 'subreddit'),
            'display_name',
            ''
        )
        self.author = getattr(
            getattr(submission, 'author'),
            'name',
            'u_deleted'
        )
        self.media_type = Post.get_media_type(submission)
        self.nsfw = getattr(submission, 'over_18', False)
        if self.media_type == MediaType.VIDEO:
            self.is_removed = not bool(self.media)
        elif self.media_type == MediaType.GALLERY:
            self.is_removed = not bool(
                self.media_metadata and self.gallery_data
            )
        else:
            self.is_removed = bool(getattr(
                submission,
                'removed_by_category',
                False
            ))

    def do_asserts(self):
        assert self.media_type != MediaType.UNKNOWN, \
            f"Post is of unsupported type"
        assert not self.is_removed, f"Post is removed"
        assert self.url, f"Post doesn't contain a link"
        assert self.subreddit, f"Failed retrieving subreddit name"

    @staticmethod
    def get_media_type(sub: Submission):
        if getattr(sub, 'fullname')[:3] == 't1_':
            return MediaType.COMMENT

        if not isinstance(sub, Submission) or not getattr(sub, 'fullname', '')[:3] == 't3_':
            return MediaType.UNKNOWN

        if getattr(sub, 'is_self', False) or hasattr(sub, 'poll_data'):
            return MediaType.UNKNOWN

        if getattr(sub, 'is_gallery', False):
            return MediaType.GALLERY

        elif getattr(sub, 'is_video', False):
            return MediaType.VIDEO

        url = getattr(sub, 'url', '')
        if re.search(r'\.jpg|\.jpeg|\.png', url):
            return MediaType.IMAGE

        elif re.search(r'\.gif|\.gifv', url):
            return MediaType.IMAGE

        elif '/gallery/' in url:
            return 'gallery'

        elif 'i.redd.it' in url:
            return MediaType.IMAGE

        elif 'v.redd.it' in url:
            return MediaType.VIDEO

        return MediaType.UNKNOWN

    def __str__(self) -> str:
        attribs = [
            f'ID: {self.id}',
            f'Title: {self.title}',
            f'Author: {self.author}',
            f'Subreddit: {self.subreddit}',
            f'Url: {self.url}',
        ]
        return '\n'.join(attribs)

    def __repr__(self) -> str:
        return f'<Post {self.id}/>'
