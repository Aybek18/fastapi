from dataclasses import dataclass

from sqlalchemy.orm import Session

from core.exceptions import EventAppUserNotFound
from core.repositories import BaseRepository
from users.models import User


@dataclass
class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_user_by_phone_number(self, phone_number: str, db: Session()):
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if isinstance(user, User):
            return user
        raise EventAppUserNotFound()
    @classmethod
    def factory(cls) -> "UserRepository":
        return cls()
