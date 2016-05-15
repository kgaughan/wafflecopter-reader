"""\
Fetch feeds pending update.

Usage:
  wc-fetch
  wc-fetch -h | --help

Options:
  -h, --help         Show this screen and exit.
"""

import datetime
import sys

import docopt
import feedparser

from wafflecopter import models


def main():
    args = docopt.docopt(__doc__)
    to_update = (models.Feed
                 .select()
                 .where((models.Feed.next_fetch <= datetime.datetime.utcnow()) |
                        (models.Feed.next_fetch == None)))
    for feed in to_update:
        print "Updating '%s' from %s" % (feed.title, feed.url)
        # parse(url_file_stream_or_string,
        #       etag=None, modified=None, agent=None, referrer=None,
        #       handlers=None, request_headers=None, response_headers=None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
