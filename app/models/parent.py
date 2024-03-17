"""Database parent models."""

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType

from app.models.base import PersonBaseModel

if TYPE_CHECKING:
    from app.models.associations import ChildParentAssociation
    from app.models.child import Child


class Parent(PersonBaseModel):
    """Application parent."""

    __tablename__ = "parents"

    email: Mapped[str] = mapped_column(EmailType, unique=True)

    children: Mapped[List["Child"]] = relationship(
        secondary="child_parent_association",
        back_populates="parents",
        overlaps="child,parent_associations,parent",
    )
    child_associations: Mapped[List["ChildParentAssociation"]] = relationship(
        back_populates="parent", overlaps="children,parents"
    )

    def __str__(self) -> str:
        return self.family_name + " " + self.first_name
