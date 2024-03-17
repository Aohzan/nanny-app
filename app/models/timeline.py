"""Database timeline models."""

import datetime
import enum
from typing import TYPE_CHECKING, List

import humanize
from flask_babel import lazy_gettext as _
from sqlalchemy.orm import Mapped, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.associations import TimelineMessageChildAssociation
    from app.models.child import Child


class TimelineMessageType(enum.Enum):
    """Represent a message type."""

    ARRIVAL = "Arrival"
    DEPARTURE = "Departure"
    BOTTLE = "Bottle"
    FOOD = "Food"
    ACTIVITY = "Activity"


class TimelineMessage(BaseModel):
    """Represent a Message in a timeline."""

    __tablename__ = "timeline_message"

    message_type: Mapped[TimelineMessageType]

    @property
    def message_type_name(self) -> str:
        """Return name type."""
        return _(self.message_type.value)

    @property
    def message_type_icon(self) -> str:
        """Return icon associated to the type."""
        match self.message_type.name:
            case TimelineMessageType.ARRIVAL:
                return "clock"
            case TimelineMessageType.DEPARTURE:
                return "clock-rotate-left"
            case TimelineMessageType.BOTTLE:
                return "bottle-water"
            case TimelineMessageType.FOOD:
                return "utensils"
            case TimelineMessageType.ACTIVITY:
                return "child-reaching"
        return "comment"

    message: Mapped[str | None]
    duration_minutes: Mapped[int | None]
    quantity: Mapped[int | None]

    children: Mapped[List["Child"]] = relationship(
        secondary="timeline_message_child_association",
        back_populates="timeline_messages",
        overlaps="child,timeline_message_associations,timeline_message",
    )
    child_associations: Mapped[List["TimelineMessageChildAssociation"]] = relationship(
        back_populates="timeline_message", overlaps="children,timeline_messages"
    )

    @property
    def children_names(self) -> str:
        """Return readable children names in a string."""
        return ", ".join([str(c) for c in self.children])

    @property
    def added_date_readable(self) -> str:
        """Readable added date."""
        return (
            humanize.naturaltime(datetime.datetime.now() - self.added_date)
            + " | "
            + self.added_date.strftime("%H:%M")
        )

    @property
    def duration_readable(self) -> str | None:
        """Readable duration."""
        if self.duration_minutes:
            return humanize.naturaldelta(
                datetime.timedelta(minutes=self.duration_minutes)
            )
        return None
