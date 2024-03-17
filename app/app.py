"""The flask app."""

import os

from flask import Flask, g, request, session
from flask_babel import Babel
from flask_humanize import Humanize

from app.config import Config as baseConfig
from app.db import db
from app.db_init import fill_db_test_data, init_db
from app.views.admin import admin_blueprint
from app.views.base import base_blueprint
from app.views.child import child_blueprint
from app.views.timeline import timeline_blueprint
from app.views.parent import parent_blueprint


def get_locale() -> str:
    """Return parent's language from session, parent config or browser."""
    if session.get("language"):
        return session.get("language")
    parent = getattr(g, "parent", None)
    if parent is not None:
        return parent.language
    return request.accept_languages.best_match(["fr", "en"])


def get_timezone() -> str | None:
    """Return parent's timezone."""
    parent = getattr(g, "parent", None)
    if parent is not None:
        return parent.timezone
    return None


def create_app(test_config=None) -> Flask:
    """Create Flask app."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(baseConfig)
    if test_config is None:
        app.config.from_prefixed_env()
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)

    humanize = Humanize(app)

    @humanize.localeselector
    def get_humanize_locale() -> str:
        return get_locale()

    with app.app_context():
        db.init_app(app)

        app.register_blueprint(base_blueprint)
        app.register_blueprint(admin_blueprint)
        app.register_blueprint(timeline_blueprint)
        app.register_blueprint(parent_blueprint)
        app.register_blueprint(child_blueprint)

        if app.debug or app.testing:
            db.drop_all()

        db.create_all()
        init_db()

        if app.debug or app.testing:
            fill_db_test_data()

        return app
