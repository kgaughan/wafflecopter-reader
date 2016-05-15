"""\
Import/export an OPML file for a given user.

Usage:
  wc-opml import --user=<username> <file>
  wc-opml export --user=<username>
  wc-opml -h | --help

Options:
  -h, --help         Show this screen and exit.
  --user=<username>  Username of user to import/export subscriptions for.
"""

import sys

from adjunct import opml
import docopt

from wafflecopter import models


def import_opml(user, outline):
    """
    Import the given OPML file for the given user.
    """
    if outline.attrs.get('type') == 'rss':
        url = outline.attrs.get('xmlUrl')
        title = outline.attrs.get('text')
        if url is not None:
            feed, _ = models.Feed.get_or_create(title=title, url=url)
            models.Subscription.create_or_get(user=user, feed=feed)
    for child in outline:
        import_opml(user, child)


def export_opml(user):
    pass


def main():
    args = docopt.docopt(__doc__)

    try:
        user = models.User.get(username=args['--user'])
    except models.User.DoesNotExist:
        print >> sys.stderr, "Unknown user: %s" % args['--user']
        return 1

    if args['import']:
        try:
            with open(args['<file>'], 'r') as fh:
                contents = fh.read()
        except IOError as exc:
            print >> sys.stderr, exc
            return 1
        with models.db.database.atomic():
            return import_opml(user, opml.parse_string(contents))
    elif args['export']:
        return export_opml(user)

    return 0


if __name__ == '__main__':
    sys.exit(main())
