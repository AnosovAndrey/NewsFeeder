#!/usr/bin/env python3
import time
import re

from common.feed_element import FeedElement
from imports.mock_import import MockImport
from imports.twitter_import import TwitterImport
from imports.youtube_import import YouTubeImport
from exports.stupid_html_export import StupidHtmlExport
from storage.inmemory_storage import InmemoryStorage

def inspect_element(r):
    print(r.date, r.author)
    print(r.body)
    print(r.images)
    print(r.videos)
    if r.nested:
        print("Original message:")
        inspect_element(r.nested)

imports = [TwitterImport('elonmusk')]
exports = [StupidHtmlExport("export.html")]
storage = InmemoryStorage()

while True:
    for i in imports:
        result = i.get_elements(10)

        for r in result:
            inspect_element(r)
            print()
            storage.add_element(i.get_key(), r)

            # TODO: add check for duplicated items somewhere (most likely as filter request to storage)
            for e in exports:
                e.export(r)

    # sleep for 30 seconds to avoid flood with mock stuff
    time.sleep(30)
