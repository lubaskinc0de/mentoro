from datetime import datetime, timezone
from uuid import UUID

import jwt


class AccessTokenEncoder:
    def encrypt(self, unique_id: UUID) -> str:
        exp = datetime.now(tz=timezone.utc)
        return jwt.encode(
            {
                "exp": exp,
                "iat": datetime.now(tz=timezone.utc),
                "sub": str(unique_id),
            },
            "test",
            algorithm="HS256",
        )

    def decrypt(self, token: str) -> UUID:
        return UUID((jwt.decode(token, "test", algorithms=["HS256"]))["sub"])
