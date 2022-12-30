from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from database.models import Base

if TYPE_CHECKING:
    from .user import User

class Role(Base):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=50), nullable=False)
    description = Column(String(length=100))

    users: List["User"] = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(name='{self.name}', description='{self.description}')>"
