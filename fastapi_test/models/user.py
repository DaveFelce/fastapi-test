from sqlalchemy import Column, Integer, String

from fastapi_test.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String)

    __mapper_args__ = {"eager_defaults": True}
