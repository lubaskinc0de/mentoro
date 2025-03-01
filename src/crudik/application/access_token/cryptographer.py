from uuid import UUID

from cryptography.fernet import Fernet

from crudik.models.access_token import AccessToken


class AccessTokenCryptographer:
    def __init__(self, fernet: Fernet) -> None:
        self._fernet = fernet

    def crypto(self, access_token: AccessToken) -> str:
        return self._fernet.encrypt(str(access_token.id).encode("utf-8")).decode("utf-8")

    def decrypto(self, raw_session_id: str) -> UUID:
        return UUID(self._fernet.decrypt(raw_session_id).decode("utf-8"))
