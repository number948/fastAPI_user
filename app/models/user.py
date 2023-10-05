from app.database import Base
from sqlalchemy import (Column, Integer, String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)
