from downloader import Downloader
from database import Database
from config import get_config
import praw
from post import Post
from post import MediaType


def main():
    config = get_config()
    if not config:
        return
    db = Database()
    downloader = Downloader(config['download_dir'])

    try:
        print('Loading reddit client...')
        reddit = praw.Reddit(**config)
        user = reddit.user.me()
        saved_items = user.saved(limit=None)
    except Exception as e:
        print(e)
        print('Error: Authorization failed.')
        return

    downloaded = 0
    total = 0
    for submission in saved_items:
        total += 1
        try:
            if hasattr(submission, 'crosspost_parent'):
                op_id = submission.crosspost_parent.split('_')[1]
                post = Post(reddit.submission(id=op_id))
            else:
                post = Post(submission)

            if db.exists(post):
                print(f'Skipping: {post.id} - {post.title} (Already downloaded.)')
                continue
            elif post.media_type == MediaType.COMMENT:
                print(f'Skipping: {post.id} - {post.title} (Post is a comment.)')
                continue

            print('\nDownloading...')
            print(str(post))
            if post.is_removed and config['unsave_removed_post']:
                submission.unsave()
                print('Post is unsaved.')
                continue
            post.do_asserts()

            paths = downloader.download(post)
            print('Downloaded successfully.')
            downloaded += 1
            db.add(post, paths)
            if config['unsave_after_download']:
                submission.unsave()
        except KeyboardInterrupt:
            print('Error: Cancelled by user')
            break
        except Exception as e:
            print(f'Error: {e}')
    print(f'\nDownloaded {downloaded}/{total}')
    db.close()


if __name__ == '__main__':
    main()
