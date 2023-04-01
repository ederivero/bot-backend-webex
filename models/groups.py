from db import conexion
from sqlalchemy import Column, types
from uuid import uuid4
from datetime import datetime


class Group(conexion.Model):
    id = Column(type_=types.String, default=uuid4, primary_key=True)
    name = Column(type_=types.String, nullable=False)
    channel = Column(type_=types.String, unique=True, nullable=False)
    createdAt = Column(type_=types.DateTime(
        timezone=False), default=datetime.utcnow)

    __tablename__ = 'groups'
