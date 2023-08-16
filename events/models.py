import enum

from sqlalchemy import String, Column, Text, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base_class import Base
from core.models import TimestampedMixin


class EventType(enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class Event(TimestampedMixin, Base):
    title = Column(String(length=100), nullable=False, name="Название")
    photo_url = Column(String(), nullable=True, name="Фото")
    description = Column(Text(), nullable=False, name="Описание")
    date = Column(DateTime(), nullable=False, name="Дата мероприятия")
    address = Column(String(length=70), nullable=False, name="Место проведения")
    comment = Column(Text(), nullable=True, name="Комментарий")
    type = Column(Enum(EventType), nullable=False, name="Тип мероприятия")
    owner_id = Column(Integer(), ForeignKey("user.id"))
    owner = relationship("User", back_populates="event")
    