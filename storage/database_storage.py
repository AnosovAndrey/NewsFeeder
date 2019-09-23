import sqlite3
import hashlib
import base64

from storage.storage_base import StorageBase

class DatabaseStorage(StorageBase):
    def __init__(self):
        self.connection = sqlite3.connect('posts_storage.sqlite')
        self._cursor = self.connection.cursor()
        self._cursor.executescript('''CREATE TABLE IF NOT EXISTS posts
            (ID TEXT PRIMARY KEY     NOT NULL,
            AUTHOR           TEXT,
            BODY           TEXT,
            DATE           TEXT    NOT NULL,
            NESTED           TEXT);
            CREATE TABLE IF NOT EXISTS images
            (ID TEXT     NOT NULL,
            IMAGE BLOB PRIMARY KEY   NOT NULL);              
            CREATE TABLE IF NOT EXISTS videos
            (ID TEXT     NOT NULL,
            VIDEO BLOB PRIMARY KEY    NOT NULL);''')        
        self.connection.commit()

    def add_element(self, service_key, feed_element):
        id = self.get_id(service_key, feed_element)
        nested_id = None
        if(feed_element.nested):
            nested_id = self.get_id(service_key, feed_element.nested)
            self._cursor.execute("INSERT or IGNORE INTO posts (ID, AUTHOR, BODY, DATE, NESTED) \
                VALUES (?, ?, ?, ?, ?)", (nested_id, feed_element.nested.author, feed_element.nested.body, feed_element.nested.date, "Nested"))
            self.add_image_or_video(nested_id, feed_element.nested)
        self.add_image_or_video(id, feed_element)
        self._cursor.execute("INSERT or IGNORE INTO posts (ID, AUTHOR, BODY, DATE, NESTED) \
            VALUES (?, ?, ?, ? , ?)", (id, feed_element.author, feed_element.body, feed_element.date, nested_id))
        self.connection.commit()
    
    def get_id(self, service_key, feed_element):
        body = (feed_element.body if feed_element.body else "") + \
            (feed_element.nested.body if feed_element.nested else "") + \
            feed_element.date + feed_element.author
        key = service_key + hashlib.md5(body.encode('utf-8')).hexdigest()
        return key
    
    def add_image_or_video(self, id, feed_element):
        if(feed_element.images):
            for val in feed_element.images:
                self._cursor.execute("INSERT or IGNORE INTO images (ID,  IMAGE) \
                    VALUES (?, ?)", (id, val.file_contents))
        if(feed_element.videos):
            for val in feed_element.videos:
                self._cursor.execute("INSERT or IGNORE INTO videos (ID,  VIDEO) \
                    VALUES (?, ?)", (id, val.url_address))

    def find_elements(self, service_key, filter_lambda):
        sqlstr = 'SELECT * FROM posts_storage WHERE type=''table'' AND name=''posts''' + filter_lambda + ' ORDER BY Name'
        return self._cursor.execute(sqlstr)
    
    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()