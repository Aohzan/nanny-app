"""Base views."""

from flask import Blueprint, flash, redirect, request, url_for
from flask.typing import ResponseReturnValue
from flask_babel import gettext
from sqlalchemy import select

from app.db import db
from app.forms.child import EditChildFamilyForm
from app.models.child import ChildFamilyField
from app.tools import templated

admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/admin/childf")
@templated("admin/child_family_form.html")
def child_family_form_list() -> ResponseReturnValue:
    """Show fields in family form for editing."""
    forms = []
    for field in db.session.scalars(select(ChildFamilyField)).all():
        field_form = EditChildFamilyForm(
            field_disabled=field.disabled,
            field_id=str(field.id),
            field_name=field.name,
            field_type=field.type,
        )
        field_form.field_type.render_kw = {"disabled": ""}
        if field.disabled:
            field_form.field_name.render_kw = {"disabled": ""}
        forms.append(field_form)
    new_form = EditChildFamilyForm()
    return {"title": gettext("Edit child"), "forms": forms, "new_form": new_form}


@admin_blueprint.route("/admin/childf/create", methods=["POST"])
def child_family_form_field_create() -> ResponseReturnValue:
    """Create field of family form."""
    form = EditChildFamilyForm(request.form)
    if form.validate_on_submit():
        field = ChildFamilyField(
            type=form.field_type.data,
            name=form.field_name.data,
        )
        field.save()
        flash(gettext("Field added"))
    return redirect(url_for(".child_family_form_list"))


@admin_blueprint.route("/admin/childf/edit/<field_id>", methods=["POST"])
def child_family_form_field_edit(field_id: str) -> ResponseReturnValue:
    """Edit field of family form."""
    form = EditChildFamilyForm(request.form)
    if form.validate_on_submit():
        field = db.get_or_404(ChildFamilyField, int(field_id))
        field.name = form.field_name.data
        field.save()
        flash(gettext("Field edited"))
    return redirect(url_for(".child_family_form_list"))


@admin_blueprint.route("/admin/childf/disable/<field_id>")
def child_family_form_field_disable(field_id: str) -> ResponseReturnValue:
    """Disable family form's field."""
    field = db.get_or_404(ChildFamilyField, int(field_id))
    field.disable_entity()
    flash(gettext("Field disabled"))
    return redirect(url_for(".child_family_form_list"))


@admin_blueprint.route("/admin/childf/enable/<field_id>")
def child_family_form_field_enable(field_id: str) -> ResponseReturnValue:
    """Enable family form's field."""
    field = db.get_or_404(ChildFamilyField, int(field_id))
    field.enable_entity()
    flash(gettext("Field enabled"))
    return redirect(url_for(".child_family_form_list"))
