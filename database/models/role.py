from typing import TYPE_CHECKING
from typing import List
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from database.models.base import Base

if TYPE_CHECKING:
    from .user import User

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(length=100))

    users: Mapped[List["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"<Role(name='{self.name}', description='{self.description}')>"
