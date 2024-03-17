"""Database common models."""

import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db


class BaseModel(db.Model):
    """Model with base attributes."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    added_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=E1102
    )
    added_by: Mapped[str] = mapped_column(default="admin")

    updated_date: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),  # pylint: disable=E1102
    )
    updated_by: Mapped[str] = mapped_column(default="admin")

    disabled: Mapped[bool] = mapped_column(default=False)
    disabled_by: Mapped[str] = mapped_column(default="admin")
    disabled_date: Mapped[datetime.datetime | None]

    def disable_entity(self, commit=True):
        """Mark entity as disabled with current date."""
        self.disabled = True
        self.disabled_date = datetime.datetime.now()
        if commit:
            db.session.commit()

    def enable_entity(self, commit=True):
        """Mark entity as enabled."""
        self.disabled = False
        if commit:
            db.session.commit()

    def before_save(self, *args, **kwargs):
        """Executed before saving the entity."""

    def after_save(self, *args, **kwargs):
        """Executed after saving the entity."""

    def save(self, commit=True):
        """Save the entity."""
        self.before_save()
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        self.after_save()

    def before_update(self, *args, **kwargs):
        """Executed before updating the entity."""

    def after_update(self, *args, **kwargs):
        """Executed before updating the entity."""

    def update(self, *args, **kwargs):
        """Update the entity."""
        self.before_update(*args, **kwargs)
        db.session.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        """Delete the entity."""
        db.session.delete(self)
        if commit:
            db.session.commit()


class PersonBaseModel(BaseModel):
    """Base model for persons."""

    __abstract__ = True

    first_name: Mapped[str]
    family_name: Mapped[str]

    def before_save(self, *args, **kwargs):
        """Format names."""
        self.first_name = self.first_name.capitalize()
        self.family_name = self.family_name.upper()

    def after_update(self, *args, **kwargs):
        """Format names."""
        self.first_name = self.first_name.capitalize()
        self.family_name = self.family_name.upper()
