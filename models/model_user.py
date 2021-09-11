from sqlalchemy import Column, String

from db.base_class import Base


class User(Base):
    email = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
