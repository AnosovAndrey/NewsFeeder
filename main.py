#!/usr/bin/env python3
import time
import re
import threading

from common.feed_element import FeedElement
from imports.mock_import import MockImport
from imports.twitter_import import TwitterImport
from imports.youtube_import import YouTubeImport
from imports.facebook_import import FacebookImport
from imports.vk_import import VKImport

from exports.stupid_html_export import StupidHtmlExport
from storage.inmemory_storage import InmemoryStorage
from storage.database_storage import DatabaseStorage

#from exports.webApp import app

# if __name__ == '__main__':
#     #app.run(debug=True).start()
#     threading.Thread(target=app.run).start()


def inspect_element(r):
    print(r.date, r.author)
    print(r.body)
    print(r.images)
    print(r.videos)
    if r.nested:
        print("Original message:")
        inspect_element(r.nested)


imports = [VKImport('190868')]
exports = [StupidHtmlExport("export.html")]
#storage = InmemoryStorage()
storage  = DatabaseStorage()

while True:
    for i in imports:
        result = i.get_elements(5)

        for r in result:
            #inspect_element(r)
            print()
            storage.add_element(i.get_key(), r)

            # TODO: add check for duplicated items somewhere (most likely as filter request to storage)
            for e in exports:
                e.export(r)

    # sleep for 30 seconds to avoid flood with mock stuff
    time.sleep(30)
