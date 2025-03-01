from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from crudik.application.access_token.errors import AccessTokenExpiredError
from crudik.models.base import Base


class AccessToken(Base):
    __tablename__ = "sessions"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    entity_id: Mapped[UUID] = mapped_column(nullable=False)
    revoked: Mapped[bool] = mapped_column(nullable=False)
    expires_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def verify(self) -> None:
        if self.expires_in < datetime.now(tz=UTC) or self._revoked:
            raise AccessTokenExpiredError(self)

    def revoke(self) -> None:
        self._revoked = True
