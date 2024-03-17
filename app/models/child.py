"""Database child models."""

import datetime
from typing import TYPE_CHECKING, List

from flask_babel import gettext
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import ChildFamilyFieldAssociation
from app.models.base import BaseModel, PersonBaseModel

if TYPE_CHECKING:
    from app.models.associations import (
        ChildParentAssociation,
        TimelineMessageChildAssociation,
    )
    from app.models.timeline import TimelineMessage
    from app.models.parent import Parent


class Child(PersonBaseModel):
    """Application child."""

    __tablename__ = "children"

    # https://en.wikipedia.org/wiki/ISO/IEC_5218
    # 0 = Not known; 1 = Male; 2 = Female; 9 = Not applicable
    gender_iso: Mapped[int] = mapped_column(default=0)
    birthdate: Mapped[datetime.date]
    reside_with_both_parents: Mapped[bool | None]
    reside_schedule: Mapped[str | None]

    parents: Mapped[List["Parent"]] = relationship(
        secondary="child_parent_association",
        back_populates="children",
        overlaps="parent,child",
    )
    parent_associations: Mapped[List["ChildParentAssociation"]] = relationship(
        back_populates="child", overlaps="parents"
    )

    timeline_messages: Mapped[List["TimelineMessage"]] = relationship(
        secondary="timeline_message_child_association",
        back_populates="children",
        overlaps="timeline_message,child",
    )
    timeline_message_associations: Mapped[List["TimelineMessageChildAssociation"]] = (
        relationship(back_populates="child", overlaps="timeline_messages")
    )

    child_family_field_associations: Mapped[List["ChildFamilyFieldAssociation"]] = (
        relationship()
    )

    @property
    def gender(self) -> str:
        """Return readable gender from iso convention."""
        if self.gender_iso == 1:
            return gettext("Boy")
        if self.gender_iso == 2:
            return gettext("Girl")
        return gettext("Not defined")

    def __str__(self) -> str:
        return self.first_name.capitalize()


class ChildFamilyField(BaseModel):
    """Field for the child family form."""

    __tablename__ = "child_family_field"

    name: Mapped[str]
    type: Mapped[str]
