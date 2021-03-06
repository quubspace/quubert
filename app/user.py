import logging

from typing import Tuple, Union, List, Optional
from app.database.models import User as UserModel
from dataclasses import dataclass
from app import bot


@dataclass
class User:
    id: int
    name: str
    email: str
    db_object: UserModel

    @classmethod
    async def load(
        cls,
        user_id: int = None,
        name: str = None,
        email: str = None,
        user_obj: UserModel = None,
        db_object: bool = False,
    ) -> Union["User", Tuple["User", UserModel]]:
        """Load a user through user_id or the user_obj database objects.
        If db_object flag is enabled, the method will also return the db_object."""
        if user_obj:
            user_db = user_obj
        else:
            try:
                user_db = bot.user_data[user_id]
            except Exception as e:
                logging.info(f"Excepting, continuing to create model: {e}")
                bot.user_data[user_id] = await UserModel.create(
                    id=user_id, name=name, email=email
                )
                user_db = bot.user_data[user_id]
        user = cls(
            id=user_db.id,
            name=user_db.name,
            email=user_db.email,
            db_object=bot.user_data[user_id],
        )
        if db_object:
            return user, user_db
        else:
            return user

    async def update_email(self, new_email: str) -> None:
        await self.db_object.update(email=new_email).apply()
        bot.user_data[self.id].email = new_email

    async def update_name(self, new_name: str) -> None:
        await self.db_object.update(name=new_name).apply()
        bot.user_data[self.id].name = new_name
