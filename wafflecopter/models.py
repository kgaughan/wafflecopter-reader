import peewee
from playhouse import flask_utils


db = flask_utils.FlaskDB()


class User(db.Model):
    """
    A user.
    """

    username = peewee.CharField()


class Feed(db.Model):
    """
    A feed we monitor.
    """

    # Name of the feed.
    title = peewee.CharField()
    # URL of the feed.
    url = peewee.CharField(unique=True)
    # URL of the associated site.
    site_url = peewee.CharField(null=True)
    # When the feed was last fetched.
    last_fetched = peewee.DateTimeField(null=True)
    # When the feed is scheduled to be fetched again.
    next_fetch = peewee.DateTimeField(null=True, index=True)
    # Number of minute between fetches.
    period = peewee.IntegerField(default=60)

    # Headers for performing conditional GET requests.
    http_etag = peewee.CharField(null=True)
    http_last_modified = peewee.CharField(null=True)


class Subscription(db.Model):
    """
    A feed subscription.
    """

    user = peewee.ForeignKeyField(User, related_name='subscriptions')
    feed = peewee.ForeignKeyField(Feed)

    class Meta:
        primary_key = peewee.CompositeKey('user', 'feed')


def create_tables():
    """
    Create the application's tables.
    """
    db.database.create_tables([Feed, User, Subscription])


def preload():
    """
    Preload the database with some development data.
    """
    User.create(username='keith')


if __name__ == '__main__':
    create_tables()
    preload()
