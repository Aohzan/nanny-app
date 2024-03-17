"""Feed views."""

from flask import Blueprint, redirect, request, url_for
from flask.typing import ResponseReturnValue
from flask_babel import gettext
from flask_babel import lazy_gettext as _
from sqlalchemy import select

from app.db import db
from app.forms.timeline import TimelineMessageForm
from app.models.child import Child
from app.models.timeline import TimelineMessage
from app.tools import templated

timeline_blueprint = Blueprint("timeline", __name__)


@timeline_blueprint.route("/timeline")
@templated("timeline/list.html")
def timeline() -> ResponseReturnValue:
    """Feed messages."""
    timeline_messages = db.session.scalars(
        select(TimelineMessage)
        .where(TimelineMessage.disabled.is_(False))
        .order_by(TimelineMessage.added_date.desc())
    )
    return {
        "title": gettext("Home"),
        "timeline_messages": timeline_messages,
    }


@timeline_blueprint.route("/timeline/create", methods=["GET", "POST"])
@templated("timeline/create.html")
def timeline_create() -> ResponseReturnValue:
    """Add a message to the timeline."""
    form = TimelineMessageForm(request.form)

    form.children_ids.choices = [
        (c.id, str(c))
        for c in db.session.scalars(
            select(Child).where(Child.disabled.is_(False)).order_by(Child.first_name)
        ).all()
    ]

    if request.method == "POST" and form.validate():
        children = []
        for child_id in form.children_ids.data:
            children.append(db.get_or_404(Child, child_id))
        message = TimelineMessage(
            message_type=form.message_type.data,
            message=form.message.data,
            duration_minutes=form.duration_minutes.data,
            quantity=form.quantity.data,
            added_date=form.added_date.data,
            children=children,
        )
        message.save()
        return redirect(url_for(".timeline"))

    return {"title": _("Add message"), "form": form}
