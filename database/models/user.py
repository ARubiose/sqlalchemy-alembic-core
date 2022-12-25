from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database.models import Base

class User(Base):
    __tablename__ = "users"
    
    id          = Column(BigInteger, primary_key=True)
    name        = Column(String(length=20), nullable=False)
    fullname    = Column(String(length=50), nullable=False)
    password    = Column(String(length=128), nullable=False)

    role_id     = Column(BigInteger, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    addresses = relationship("Address", back_populates="users")

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}')>"