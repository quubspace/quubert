from dataclasses import dataclass
from datetime import datetime
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
        hours_obj: HoursModel = None,
        db_object: bool = False,
    ) -> Union["Hours", Tuple["Hours", HoursModel]]:
        """Load an hours object through user_id or the hours_obj database objects.
        If db_object flag is enabled, the method will also return the db_object."""
        if hours_obj:
            hours_db = hours_obj
        else:
            try:
                hours_db = bot.hours_data[user_id]
            except KeyError:
                bot.hours_data[user_id] = await HoursModel.create(
                    id=user_id,
                    quantity=quantity,
                    description=description,
                    date=date,
                )
                hours_db = bot.hours_data[user_id]
        hours = cls(
            id=hours_db.id,
            user_id=hours_db.user_id,
            quantity=hours_db.quantity,
            description=hours_db.description,
            date=hours_db.date,
            db_object=bot.hours_data[user_id],
        )
        if db_object:
            return hours, hours_db
        else:
            return hours
