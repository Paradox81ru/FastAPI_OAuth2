from datetime import datetime
from db.database import Base
from sqlalchemy import func
from sqlalchemy import String, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import selectinload, joinedload, contains_eager


class User(Base):
    __tablename__ = 'accounts_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(60), default="")
    last_name: Mapped[str | None] = mapped_column(String(60), default="")
    email: Mapped[str] = mapped_column(String(254))
    status: Mapped[int] = mapped_column(SMALLINT)
    role: Mapped[int] = mapped_column(SMALLINT)
    date_joined: Mapped[datetime] = mapped_column(default=func.now())
    last_login: Mapped[datetime | None]

