import os

import flask


def create_app():
    app = flask.Flask("wafflecopter")

    app.config.update(
        DEBUG=False,
        SECRET_KEY="DEADMEATDEADMEATDEADMEAT",
        DATABASE="sqlite:///wafflecopter.db",
        THREADPOOL_MAX=8,
    )
    if "WAFFLECOPTER_SETTINGS" in os.environ:
        app.config.from_envvar("WAFFLECOPTER_SETTINGS")

    from wafflecopter import models

    models.db.init_app(app)

    return app


app = create_app()
