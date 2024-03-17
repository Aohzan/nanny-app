"""Children views."""

import wtforms
from flask import Blueprint, flash, redirect, request, url_for
from flask.typing import ResponseReturnValue
from flask_babel import gettext
from sqlalchemy import select

from app.db import db
from app.forms.child import ChildForm, DynamicChildFamilyForm
from app.models.associations import ChildFamilyFieldAssociation, ChildParentAssociation
from app.models.child import Child, ChildFamilyField
from app.models.parent import Parent
from app.tools import templated

child_blueprint = Blueprint("child", __name__)


@child_blueprint.route("/children/")
@child_blueprint.route("/children")
@templated("child/list.html")
def children_list() -> ResponseReturnValue:
    """Show children."""
    children = db.session.scalars(
        select(Child).where(Child.disabled.is_(False)).order_by(Child.first_name)
    )
    return {
        "title": gettext("Children"),
        "children": children,
    }


@child_blueprint.route("/child/create", methods=["GET", "POST"])
@templated("child/create.html")
def child_create() -> ResponseReturnValue:
    """Create child."""
    form = ChildForm(request.form)
    if request.method == "POST" and form.validate():
        child = Child()
        form.populate_obj(child)
        # child = Child(
        #     first_name=form.first_name.data,
        #     family_name=form.family_name.data,
        #     gender_iso=form.gender_iso.data,
        #     birthdate=form.birthdate.data,
        #     reside_with_both_parents=form.reside_with_both_parents.data,
        #     reside_schedule=form.reside_schedule.data,
        # )
        child.save()
        flash(gettext("Child successfully added."), category="success")
        return redirect(url_for(".child_detail", child_id=child.id))

    return {"title": gettext("Add child"), "form": form}


@child_blueprint.route("/child/<int:child_id>")
@templated("child/detail.html")
def child_detail(child_id: int) -> ResponseReturnValue:
    """Show the child."""
    child = db.get_or_404(Child, child_id)
    return {
        "title": gettext("Child %(child)s", child=child),
        "child": child,
    }


@child_blueprint.route("/child/<int:child_id>/delete")
def child_delete(child_id: int) -> ResponseReturnValue:
    """Disable the child."""
    child = db.get_or_404(Child, child_id)
    child.disable_entity()
    flash(gettext("Child successfully disabled."), category="success")
    return redirect(url_for(".children_list"))


# Family form
@child_blueprint.route("/child/<int:child_id>/editf", methods=["GET", "POST"])
@templated("child/editf.html")
def child_family_edit(child_id: int) -> ResponseReturnValue:
    """Edit child from Family."""
    child = db.get_or_404(Child, child_id)
    fields = db.session.scalars(
        select(ChildFamilyField)
        .where(ChildFamilyField.disabled.is_(False))
        .order_by(ChildFamilyField.id)
    ).all()

    for field in fields:
        field_type = getattr(wtforms, field.type)
        current_value = next(
            iter(
                [
                    f.value
                    for f in child.child_family_field_associations
                    if f.child_id == child.id and f.child_family_field_id == field.id
                ]
            ),
            None,
        )
        setattr(
            DynamicChildFamilyForm,
            str(field.id),
            field_type(label=field.name, default=current_value),
        )

    form = DynamicChildFamilyForm(request.form)

    if request.method == "POST" and form.validate():
        for field in fields:
            field_value = getattr(form, str(field.id)).data
            if assoc := next(
                iter(
                    [
                        f
                        for f in child.child_family_field_associations
                        if f.child_id == child.id
                        and f.child_family_field_id == field.id
                    ]
                ),
                None,
            ):
                assoc.value = field_value
            else:
                child.child_family_field_associations.append(
                    ChildFamilyFieldAssociation(
                        child_family_field_id=field.id, value=field_value
                    )
                )
        db.session.commit()
        flash(gettext("Child successfully updated."), category="success")
        return redirect(url_for(".child_detail", child_id=child.id))

    return {"title": gettext("Edit child"), "form": form}


# Childre/Parent associations
@child_blueprint.route("/child/<int:child_id>/assoc/add", methods=["GET", "POST"])
@templated("children/assoc.html")
def child_assoc_add(child_id: int) -> ResponseReturnValue:
    """Assoc the child to a parent."""
    if request.method == "POST":
        parent = db.get_or_404(Parent, request.form["parent_id"])
        child = db.get_or_404(Child, child_id)
        child.parent_associations.append(
            ChildParentAssociation(
                parent=parent, relation_type=request.form["relation_type"]
            )
        )
        child.update()
        return redirect(url_for(".child_detail", child_id=child.id))

    child = db.get_or_404(Child, child_id)
    active_parents = db.session.scalars(
        select(Parent).where(Parent.disabled.is_(False)).order_by(Parent.family_name)
    ).all()
    select_parents = [u for u in active_parents if u not in child.parents]

    return {
        "title": gettext("Associate a parent to %(child)s", child=child),
        "child": child,
        "select_parents": select_parents,
    }


@child_blueprint.route("/child/<int:child_id>/assoc/<int:assoc_id>/delete")
def child_assoc_delete(child_id: int, assoc_id: int) -> ResponseReturnValue:
    """Delete the association between the child and a parent."""
    assoc = db.get_or_404(ChildParentAssociation, assoc_id)
    db.session.delete(assoc)
    db.session.commit()
    return redirect(url_for(".child_detail", child_id=child_id))
