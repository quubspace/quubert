from dataclasses import dataclass
from datetime import datetime, timedelta, date
from typing import List, Optional, Tuple, Union

from app import bot
from app.database.models import Hours as HoursModel


@dataclass
class Hours:
    id: int
    user_id: int
    quantity: int
    description: str
    date: datetime
    db_object: HoursModel

    @classmethod
    async def load(
        cls,
        user_id: int = None,
        quantity: int = 0,
        description: str = None,
        date: datetime = None,
    ) -> Optional[List["Hours"]]:
        """Load a list of hours objects from the last week through user_id."""
        all_hours = (
            await HoursModel.query.where(HoursModel.user_id == user_id)
            .where(HoursModel.date <= date.today())
            .where(HoursModel.date >= (date.today() - timedelta(days=7)))
            .gino.all()
        )

        return [
            cls(
                id=hours_db.id,
                user_id=hours_db.user_id,
                quantity=hours_db.quantity,
                description=hours_db.description,
                date=hours_db.date,
                db_object=hours_db,
            )
            for hours_db in all_hours
        ]

    @classmethod
    async def add(
        cls, user_id: int, quantity: int, date: datetime, description: str = None
    ) -> "Hours":
        """Add hours to database, and return Hours object."""
        bot.hours_data[user_id] = await HoursModel.create(
            user_id=user_id,
            quantity=quantity,
            description=description,
            date=date,
        )
        hours_db = bot.hours_data[user_id]

        return cls(
            id=hours_db.id,
            user_id=hours_db.user_id,
            quantity=hours_db.quantity,
            description=hours_db.description,
            date=hours_db.date,
            db_object=bot.hours_data[user_id],
        )
