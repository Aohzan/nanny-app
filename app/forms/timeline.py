"""Timeline form."""

import datetime

from flask_babel import lazy_gettext as _
from wtforms import (
    DateTimeLocalField,
    Form,
    IntegerField,
    SelectField,
    SelectMultipleField,
    TextAreaField,
    validators,
)

from app.models.timeline import TimelineMessageType


class TimelineMessageForm(Form):
    """Form for timeline message."""

    message_type = SelectField(
        label=_("Message type"),
        choices=[
            (member.value, _(name.capitalize()))
            for name, member in TimelineMessageType.__members__.items()
        ],
        validators=[validators.input_required()],
    )
    children_ids = SelectMultipleField(
        label=_("Children"),
    )
    message = TextAreaField(
        label=_("Message"),
        validators=[validators.optional()],
    )
    duration_minutes = IntegerField(
        label=_("Duration (minutes)"),
        validators=[validators.optional()],
    )
    quantity = IntegerField(
        label=_("Quantity (cl)"),
        validators=[validators.optional()],
    )
    added_date = DateTimeLocalField(
        label=_("Event date"),
        default=(datetime.datetime.now() - datetime.timedelta(minutes=5)),
    )
