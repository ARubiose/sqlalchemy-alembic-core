from typing import TYPE_CHECKING
from typing import List
from typing import Optional

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from sqltoolbox.models.base import Base

if TYPE_CHECKING:
    from .role import Role
    from .address import Address


class User(Base):
    __tablename__ = "users"

    id:        Mapped[int] = mapped_column(primary_key=True)
    name:      Mapped[str] = mapped_column(String(20), nullable=False)
    fullname:  Mapped[str] = mapped_column(String(50), nullable=False)
    password:  Mapped[str] = mapped_column(String(128), nullable=False)
    phone:     Mapped[Optional[str]] = mapped_column(String(length=20))
    photo:     Mapped[Optional[str]] = mapped_column(String(length=100))

    role_id:   Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role:      Mapped["Role"] = relationship(back_populates="users")
    addresses:  Mapped[List["Address"]] = relationship(back_populates="users")

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}')>"