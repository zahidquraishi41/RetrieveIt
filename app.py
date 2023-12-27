from downloader import Downloader
from database import Database
from config import get_config
import praw
from post import Post


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
                print(f'Skipping: {post.id} - {post.title}')
                continue
            print('\nDownloading...')
            print(str(post))
            post.do_asserts()

            downloader.download(post)
            print('Downloaded successfully.')
            downloaded += 1
            db.add_post(post)
            if config['unsave_after_download']:
                submission.unsave()
        except KeyboardInterrupt:
            print('Error: Cancelled by user')
            break
        except Exception as e:
            print(f'Error: {e}')
    print(f'Downloaded {downloaded}/{total}')
    db.close()


if __name__ == '__main__':
    main()
