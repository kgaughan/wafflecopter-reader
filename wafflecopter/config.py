import os

import flask
from playhouse.flask_utils import FlaskDB


app = flask.Flask('wafflecopter')
app.config.update(
    DEBUG=False,
    SECRET_KEY='DEADMEATDEADMEATDEADMEAT',
    DATABASE='sqlite:///wafflecopter.db',
)
if 'WAFFLECOPTER_SETTINGS' in os.environ:
    app.config.from_envvar('WAFFLECOPTER_SETTINGS')

db = FlaskDB(app)
