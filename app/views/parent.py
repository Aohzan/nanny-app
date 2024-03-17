"""Parents views."""

from flask import Blueprint, flash, redirect, request, url_for
from flask.typing import ResponseReturnValue
from flask_babel import gettext

from app.db import db
from app.forms.parent import ParentForm
from app.models.parent import Parent
from app.tools import templated

parent_blueprint = Blueprint("parent", __name__)


@parent_blueprint.route("/parents")
@templated("parent/list.html")
def parents_list() -> ResponseReturnValue:
    """List parents."""
    parents = db.session.scalars(
        Parent.query.filter_by(disabled=False).order_by(Parent.family_name)
    )
    return {"title": gettext("Parents"), "parents": parents}


@parent_blueprint.route("/parent/create", methods=["GET", "POST"])
@templated("parent/create.html")
def parent_create() -> ResponseReturnValue:
    """Create parent."""
    form = ParentForm(request.form)
    if request.method == "POST" and form.validate():
        parent = Parent(
            email=form.email.data,
            first_name=form.first_name.data,
            family_name=form.family_name.data,
        )
        parent.save()
        flash(gettext("Parent successfully added"), category="success")
        return redirect(url_for(".parent_detail", parent_id=parent.id))

    return {"title": gettext("Add parent"), "form": form}


@parent_blueprint.route("/parent/<int:parent_id>")
@templated("parent/detail.html")
def parent_detail(parent_id: int) -> ResponseReturnValue:
    """Show parents."""
    parent = db.get_or_404(Parent, parent_id)
    return {
        "title": gettext("Parent %(parent)s", parent=parent),
        "parent": parent,
    }


@parent_blueprint.route("/parent/<int:parent_id>/delete")
def parent_delete(parent_id: int) -> ResponseReturnValue:
    """Disable parent."""
    parent = db.get_or_404(Parent, parent_id)
    parent.disable_entity()
    flash(gettext("Parent successfully disabled."), category="success")
    return redirect(url_for(".parents_list"))
