"""Database data management."""

import datetime

from app.db import db
from app.models.associations import ChildFamilyFieldAssociation, ChildParentAssociation
from app.models.child import Child, ChildFamilyField
from app.models.timeline import TimelineMessage, TimelineMessageType
from app.models.parent import Parent


def init_db() -> None:
    """Populate database with initial data."""
    # Custom child families fields
    birth_story = ChildFamilyField(name="My birth story", type="TextAreaField")
    dummy = ChildFamilyField(name="Dummy or not", type="BooleanField")
    db.session.add_all(
        [
            birth_story,
            dummy,
        ]
    )
    db.session.commit()


def fill_db_test_data() -> None:
    """Populate database with demo data."""

    # family
    jeandupont = Parent(
        email="jean.dupont@mail.com", first_name="Jean", family_name="DUPONT"
    )
    mariedupont = Parent(
        email="marie.dupont@mail.com", first_name="Marie", family_name="DUPONT"
    )
    annemartin = Parent(
        email="anne.martin@mail.com", first_name="Anne", family_name="MARTIN"
    )

    # children
    enzodupont = Child(
        first_name="Enzo",
        family_name="DUPONT",
        birthdate=datetime.date(2022, 5, 17),
        parent_associations=[
            ChildParentAssociation(parent=jeandupont, relation_type="Papa"),
            ChildParentAssociation(parent=mariedupont, relation_type="Maman"),
        ],
        child_family_field_associations=[
            ChildFamilyFieldAssociation(child_family_field_id=2, value=False),
        ],
    )
    zoemartin = Child(
        first_name="Zoé",
        family_name="MARTIN",
        gender_iso=2,
        birthdate=datetime.date(2022, 10, 4),
        parent_associations=[
            ChildParentAssociation(parent=annemartin, relation_type="Maman"),
        ],
    )
    marcelmartin = Child(
        first_name="Marcel",
        family_name="MARTIN",
        gender_iso=1,
        birthdate=datetime.date(2023, 10, 17),
        parent_associations=[
            ChildParentAssociation(parent=annemartin, relation_type="Maman"),
        ],
        child_family_field_associations=[
            ChildFamilyFieldAssociation(child_family_field_id=1, value="Lorem ipsum"),
            ChildFamilyFieldAssociation(child_family_field_id=2, value=True),
        ],
    )
    db.session.add_all([jeandupont, mariedupont, annemartin])
    db.session.add_all([enzodupont, zoemartin, marcelmartin])
    db.session.commit()

    db.session.add_all(
        [
            TimelineMessage(
                children=[zoemartin, marcelmartin],
                message_type=TimelineMessageType.ARRIVAL,
                added_date=datetime.datetime.now().replace(hour=8, minute=10),
            ),
            TimelineMessage(
                children=[enzodupont],
                message_type=TimelineMessageType.ARRIVAL,
                added_date=datetime.datetime.now().replace(hour=8, minute=35),
            ),
            TimelineMessage(
                message="On joue aux LEGO",
                children=[enzodupont, zoemartin],
                message_type=TimelineMessageType.ACTIVITY,
                added_date=datetime.datetime.now().replace(
                    hour=10, minute=10, second=40
                ),
            ),
            TimelineMessage(
                children=[marcelmartin],
                message_type=TimelineMessageType.BOTTLE,
                quantity=180,
                added_date=datetime.datetime.now().replace(hour=11, minute=35),
            ),
            TimelineMessage(
                children=[enzodupont, zoemartin],
                message_type=TimelineMessageType.FOOD,
                added_date=datetime.datetime.now().replace(hour=12, minute=00),
            ),
            TimelineMessage(
                children=[enzodupont],
                message_type=TimelineMessageType.DEPARTURE,
                added_date=datetime.datetime.now().replace(hour=17, minute=4),
            ),
        ]
    )
    db.session.commit()
