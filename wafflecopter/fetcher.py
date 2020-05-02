from __future__ import print_function

import datetime
import pprint
import sys

import click
import feedparser

from wafflecopter import models


@click.command()
def main():
    """
    Fetch feeds pending update.
    """
    to_update = (models.Feed
                 .select()
                 .where((models.Feed.next_fetch <= datetime.datetime.utcnow()) |
                        (models.Feed.next_fetch == None)))
    for feed in to_update:
        print("Updating '{}' from {}".format(feed.title, feed.url), file=sys.stderr)
        # parse(url_file_stream_or_string,
        #       etag=None, modified=None, agent=None, referrer=None,
        #       handlers=None, request_headers=None, response_headers=None)
        result = feedparser.parse(feed.url,
                                  etag=feed.http_etag,
                                  modified=feed.http_last_modified)
        pprint.pprint(result)
        break
    return 0


if __name__ == '__main__':
    main()
