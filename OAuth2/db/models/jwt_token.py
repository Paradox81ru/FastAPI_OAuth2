from OAuth2.db.models import Base
from sqlalchemy import String, SMALLINT, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from OAuth2.db.models import User


class JWTToken(Base):
    __tablename__ = "accounts_jwt_token"

    jti: Mapped[str] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("accounts_user.id"))
    subject: Mapped['User'] = relationship(back_populates='jwt_tokens')
    revoked: Mapped[bool] = mapped_column(default=False)