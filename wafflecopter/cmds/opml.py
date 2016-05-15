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
    imported = 0
    if outline.attrs.get('type') == 'rss':
        site_url = outline.attrs.get('htmlUrl')
        url = outline.attrs.get('xmlUrl')
        title = outline.attrs.get('text')
        if url is not None:
            feed, _ = models.Feed.create_or_get(title=title,
                                                url=url, site_url=site_url)
            _, created = models.Subscription.create_or_get(user=user, feed=feed)
            if created:
                imported += 1
    for child in outline:
        imported += import_opml(user, child)
    return imported


def export_opml(user):
    pass


def main():
    args = docopt.docopt(__doc__)

    try:
        user = models.User.get(username=args['--user'])
    except models.User.DoesNotExist:
        print("Unknown user: {}", args['--user'], file=sys.stderr)
        return 1

    if args['import']:
        try:
            with open(args['<file>'], 'rb') as fh:
                contents = fh.read()
        except IOError as exc:
            print(exc, file=sys.stderr)
            return 1
        with models.db.database.atomic():
            imported = import_opml(user, opml.parse_string(contents))
            print("New feeds imported: {}", imported)
    elif args['export']:
        return export_opml(user)

    return 0


if __name__ == '__main__':
    sys.exit(main())
