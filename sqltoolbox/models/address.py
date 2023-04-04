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
    from .user import User

class Address(Base):
    """ adresses table """
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(length=50), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped[List["User"]] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"<Address(address='{self.address}')>"