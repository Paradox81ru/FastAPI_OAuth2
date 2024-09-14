from datetime import datetime
from OAuth2.db.models import Base
from sqlalchemy import String, SMALLINT, UUID, ForeignKey, DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from OAuth2.db.models import User


class JWTToken(Base):
    __tablename__ = "accounts_jwt_token"

    jti: Mapped[hex] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("accounts_user.id"))
    expire: Mapped[datetime] = mapped_column(DATETIME)
    subject: Mapped['User'] = relationship(back_populates='jwt_tokens')