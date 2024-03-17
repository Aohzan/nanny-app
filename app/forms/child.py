"""Child form."""

from flask_babel import gettext
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    SelectField,
    StringField,
    TextAreaField,
    ValidationError,
    validators,
)

from app.forms.base import PersonForm


class ChildForm(PersonForm):
    """Form for child creation/edit."""

    gender_iso = SelectField(
        label=_("Gender"),
        coerce=int,
        choices=[
            (0, _("Not defined")),
            (1, _("Boy")),
            (2, _("Girl")),
        ],
        validators=[validators.input_required()],
    )

    def validate_gender_iso(self, field) -> None:
        """Raise error if gender not match iso."""
        if field.data not in [0, 1, 2]:
            raise ValidationError(
                gettext("Gender must match iso: Not defined, boy or girl")
            )

    birthdate = DateField(
        label=_("Birth date"), validators=[validators.input_required()]
    )
    reside_with_both_parents = BooleanField(
        label=_("Reside with both parents"),
        validators=[validators.optional()],
    )
    reside_schedule = TextAreaField(
        label=_("Reside schedule"),
        validators=[validators.optional()],
    )


class DynamicChildFamilyForm(FlaskForm):
    """Form for child edit from Family."""


class EditChildFamilyForm(FlaskForm):
    """Form for field edit from Family."""

    field_disabled = BooleanField()
    field_id = StringField()
    field_name = StringField(
        label=_("Name"),
        validators=[validators.input_required()],
    )
    field_type = SelectField(
        label=_("Field type"),
        choices=[
            ("StringField", _("Small text")),
            ("TextAreaField", _("Large text")),
            ("BooleanField", _("Yes or no")),
        ],
        validators=[validators.input_required()],
    )
