"""Database associations models."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import db
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.child import Child, ChildFamilyField
    from app.models.timeline import TimelineMessage
    from app.models.parent import Parent


class ChildParentAssociation(BaseModel):
    """Association many-to-many between Child and Parent tables."""

    __tablename__ = "child_parent_association"

    child_id: Mapped[int] = mapped_column(ForeignKey("children.id"))
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"))
    relation_type: Mapped[str]

    child: Mapped["Child"] = relationship(back_populates="parent_associations")
    parent: Mapped["Parent"] = relationship(back_populates="child_associations")


class TimelineMessageChildAssociation(BaseModel):
    """Association many-to-many between FeedMessage and Child tables."""

    __tablename__ = "timeline_message_child_association"

    child_id: Mapped[int] = mapped_column(ForeignKey("children.id"))
    timeline_message_id: Mapped[int] = mapped_column(ForeignKey("timeline_message.id"))

    child: Mapped["Child"] = relationship(
        back_populates="timeline_message_associations"
    )
    timeline_message: Mapped["TimelineMessage"] = relationship(
        back_populates="child_associations"
    )


class ChildFamilyFieldAssociation(db.Model):
    """Association many-to-one between ChildFamilyField and Child tables."""

    __tablename__ = "child_family_field_child_association"

    child_id: Mapped[int] = mapped_column(ForeignKey("children.id"), primary_key=True)
    child_family_field_id: Mapped[int] = mapped_column(
        ForeignKey("child_family_field.id"), primary_key=True
    )
    child_family_field: Mapped["ChildFamilyField"] = relationship()
    value: Mapped[str]
