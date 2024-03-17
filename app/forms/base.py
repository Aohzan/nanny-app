"""Base form."""

from flask_babel import lazy_gettext as _
from wtforms import Form, StringField, validators


class PersonForm(Form):
    """Base form for persons."""

    __abstract__ = True

    first_name = StringField(
        label=_("First name"),
        validators=[validators.Length(min=3, max=255), validators.input_required()],
    )
    family_name = StringField(
        label=_("Family name"),
        validators=[validators.Length(min=3, max=255), validators.input_required()],
    )
