import typing
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database.models import Base

class User(Base):
    __tablename__ = "users"
    
    id          = Column(BigInteger, primary_key=True)
    name        = Column(String(length=20), nullable=False)
    fullname    = Column(String(length=50), nullable=False)
    password    = Column(String(length=128), nullable=False)
    phone       = Column(String(length=20))
    photo       = Column(String(length=100))

    role_id     = Column(BigInteger, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    addresses = relationship("Address", back_populates="users")

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        # TODO: Add validation
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}')>"

    # CRUD
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_by_attr(cls, session, attr, value):
        return session.query(cls).filter(getattr(cls, attr) == value).first()

    @classmethod
    def delete_by_id(cls, session, id):
        session.query(cls).filter(cls.id == id).delete()
        session.commit()

    @classmethod
    def delete_by_attr(cls, session, attr, value):
        session.query(cls).filter(getattr(cls, attr) == value).delete()
        session.commit()

    @classmethod
    def update_by_id(cls, session, id, **kwargs):
        session.query(cls).filter(cls.id == id).update(kwargs)
        session.commit()

    # Validation