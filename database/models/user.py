from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import relationship

from database.models import Base

class User(Base):
    __tablename__ = "users"
    
    id          = Column(Integer, Identity(start=0, cycle=True), primary_key=True)
    name        = Column(String)
    fullname    = Column(String)
    password    = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', password='{self.password}')>"