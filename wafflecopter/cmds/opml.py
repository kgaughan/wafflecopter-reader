from adjunct import opml
import click

from wafflecopter import models


def get_user(username):
    try:
        return models.User.get(username=username)
    except models.User.DoesNotExist:
        raise click.BadParameter("Unknown user: {}".format(username), param="user")


def do_import(user, outline):
    imported = 0
    if outline.attrs.get("type") == "rss":
        site_url = outline.attrs.get("htmlUrl")
        url = outline.attrs.get("xmlUrl")
        title = outline.attrs.get("text")
        if url is not None:
            feed, _ = models.Feed.create_or_get(title=title, url=url, site_url=site_url)
            _, created = models.Subscription.create_or_get(user=user, feed=feed)
            if created:
                imported += 1
    for child in outline:
        imported += import_opml(user, child)
    return imported


@click.group()
def cli():
    """
    Import/export an OPML file for a given user.
    """


@cli.command("import")
@click.option(
    "--user",
    type=str,
    required=True,
    metavar="USERNAME",
    help="User to import subscriptions for",
)
@click.argument("path")
def import_opml(user, path):
    """
    Import the given OPML file for the given user.
    """
    with open(path, "rb") as fh:
        outline = opml.parse_string(fh.read())
    with models.db.database.atomic():
        imported = do_import(get_user(user), outline)
    print("New feeds imported:", imported)


@cli.command("export")
@click.option(
    "--user",
    type=str,
    required=True,
    metavar="USERNAME",
    help="User to export subscriptions for",
)
def export_opml(user):
    """
    Export an OPML file for the given user.
    """


if __name__ == "__main__":
    cli()
