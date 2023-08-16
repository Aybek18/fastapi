from sqlalchemy import Column, String, Boolean

from core.models import TimestampedMixin
from base_class import Base


class User(TimestampedMixin, Base):
    username = Column(String(length=40), unique=True, index=True, name="Имя пользователя", nullable=False)
    photo_url = Column(String(), name="Фото пользователя", nullable=True)
    is_active = Column(Boolean, default=True, name="Статус активности")
    phone_number = Column(String(length=15), unique=True, name="Номер телефона", nullable=False)
    is_superuser = Column(Boolean(), default=False, name="Статус суперпользователя")
