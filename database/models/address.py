from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database.models import Base

class Address(Base):
    """ adresses table """
    __tablename__ = "addresses"

    id              = Column(BigInteger, primary_key=True)
    address         = Column(String(length=50), nullable=False)
    
    user_id         = Column(BigInteger, ForeignKey("users.id"))
    users = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(address='{self.address}')>"