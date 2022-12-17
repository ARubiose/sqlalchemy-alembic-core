from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import relationship

from database.models import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, Identity(start=0, cycle=True), primary_key=True)
    name = Column(String)
    description = Column(String)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(name='{self.name}', description='{self.description}')>"
