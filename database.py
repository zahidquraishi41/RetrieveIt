import sqlite3 as sql
import time
from post import Post
from typing import List

"""Database Schema
post
======
Column      Data Type   Description
id(pk)      text        unique id of post. generated by reddit side.
title       text        title of the post.
type        integer     media type of the post can be 0-3 for image, gallery & video.
url         text        url of the post.
subreddit   text        name of subreddit post belongs to.
author      text        author of the post.
upvotes     integer     post's upvote count.
created_utc integer     utc when post was created.
downloaded_utc integer  utc when post was downloaded to local storage.
"""


class Database:
    def __init__(self, path: str = 'log.db') -> None:
        self._path = path
        self._con = sql.Connection(self._path)
        self._cur = self._con.cursor()
        self._cur.execute('PRAGMA foreign_keys = ON;')
        self._create_tables()

    def add(self, post: 'Post', download_paths=List[str]):
        self._cur.execute(
            '''INSERT INTO post VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                post.id, post.title, post.media_type.value, post.url,
                post.subreddit, post.author, post.upvotes,
                post.created_utc, int(time.time())
            )
        )
        for download_path in download_paths:
            self._cur.execute(
                'INSERT INTO download VALUES (?, ?)',
                (post.id, download_path)
            )
        self._con.commit()

    def exists(self, post: Post) -> bool:
        '''Returns true if post is already added to database; otherwise false.'''
        row = self._cur.execute(
            '''SELECT * FROM post WHERE id=?''',
            (post.id, )
        ).fetchall()
        return bool(row)

    def _create_tables(self):
        '''Creates post table if not exists.'''
        post_table = '''CREATE TABLE IF NOT EXISTS post (
            id TEXT PRIMARY KEY,
            title TEXT,
            type INTEGER,
            url TEXT,
            subreddit TEXT,
            author TEXT,
            upvotes INTEGER,
            created_utc INTEGER,
            downloaded_utc INTEGER
        )'''
        download_table = '''CREATE TABLE IF NOT EXISTS download (
            id TEXT,
            path TEXT,
            FOREIGN KEY (id) REFERENCES post (id)
        )'''
        self._cur.execute(post_table)
        self._cur.execute(download_table)
        self._con.commit()

    def close(self):
        '''Closes the database'''
        self._con.close()
