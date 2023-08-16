from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql.functions import now


class TimestampedMixin(object):
    id = Column(Integer, primary_key=True, index=True, name="Id")
    created_at = Column(DateTime(), server_default=now(), name="Дата создания")
    updated_at = Column(DateTime(), server_default=now(), name="Дата обновления")
