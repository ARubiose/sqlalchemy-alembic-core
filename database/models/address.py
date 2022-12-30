from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database.models import Base

if TYPE_CHECKING:
    from .user import User

class Address(Base):
    """ adresses table """
    __tablename__ = "addresses"

    id              = Column(BigInteger, primary_key=True)
    address         = Column(String(length=50), nullable=False)
    
    user_id         = Column(BigInteger, ForeignKey("users.id"))
    users: List["User"] = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(address='{self.address}')>"