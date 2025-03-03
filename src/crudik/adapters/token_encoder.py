from datetime import datetime, timezone
from uuid import UUID

import jwt

from crudik.adapters.config import SecretConfig


class TokenEncoder:
    def __init__(self, secret: SecretConfig) -> None:
        self._secret = secret

    def encrypt(self, unique_id: UUID) -> str:
        return jwt.encode(
            {
                "iat": datetime.now(tz=timezone.utc),
                "sub": str(unique_id),
            },
            self._secret.secret_key,
            algorithm="HS256",
        )

    def decrypt(self, token: str) -> UUID:
        return UUID((jwt.decode(token, self._secret.secret_key, algorithms=["HS256"]))["sub"])
