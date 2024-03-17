"""Base views."""

from flask import Blueprint, redirect, session, url_for
from flask.typing import ResponseReturnValue
from flask_babel import gettext

from app.tools import templated

base_blueprint = Blueprint("base", __name__)


@base_blueprint.route("/")
def index() -> ResponseReturnValue:
    """Index."""
    return redirect(url_for("timeline.timeline"))


@base_blueprint.route("/contact")
@templated("contact.html")
def contact() -> ResponseReturnValue:
    """Contact."""
    return {"title": gettext("Contact")}


@base_blueprint.route("/language/<language>")
def set_language(language: str):
    """Set session language."""
    session["language"] = language
    return redirect(url_for("base.index"))
