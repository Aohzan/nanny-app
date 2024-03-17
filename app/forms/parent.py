"""Parent form."""

from flask_babel import lazy_gettext as _
from wtforms import EmailField, validators

from app.forms.base import PersonForm


class ParentForm(PersonForm):
    """Form for parent."""

    email = EmailField(
        label=_("Email"),
        validators=[validators.input_required()],
    )
