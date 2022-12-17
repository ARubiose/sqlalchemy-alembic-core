from sqlalchemy import Column, Integer, String, ForeignKey, Identity
from sqlalchemy.orm import relationship

from database.models import Base

class Address(Base):
    """ adresses table """
    __tablename__ = "addresses"

    id              = Column(Integer, Identity(start=0, cycle=True), primary_key=True)
    address         = Column(String, nullable=False)
    user_id         = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")