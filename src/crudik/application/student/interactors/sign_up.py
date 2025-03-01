from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from argon2 import PasswordHasher

from crudik.adapters.config import AccessTokenConfig
from crudik.application.access_token.cryptographer import AccessTokenCryptographer
from crudik.application.access_token.gateway import AccessTokenGateway
from crudik.application.commitable import Commitable
from crudik.application.student.gateway import StudentGateway
from crudik.application.student.validators import (
    validate_student_full_name,
    validate_student_login,
    validate_student_password,
)
from crudik.models.access_token import AccessToken
from crudik.models.student import Student


@dataclass(frozen=True, slots=True)
class SignUpStudent:
    commitable: Commitable
    cryptographer_access_token: AccessTokenCryptographer
    access_token_config: AccessTokenConfig
    access_token_gateway: AccessTokenGateway
    student_gateway: StudentGateway
    password_hasher: PasswordHasher

    async def execute(
        self,
        login: str,
        full_name: str,
        password: str,
    ) -> str:
        validate_student_login(login)
        validate_student_full_name(full_name)
        validate_student_password(password)

        student = Student(
            id=uuid4(),
            login=login,
            full_name=full_name,
            password=self.password_hasher.hash(password),
            created_at=datetime.now(tz=UTC),
        )
        access_token = AccessToken(
            id=uuid4(),
            entity_id=student.id,
            revoked=False,
            expires_in=self.access_token_config.expires_in,
            created_at=datetime.now(tz=UTC),
        )
        await self.student_gateway.add(student)
        await self.access_token_gateway.add(access_token)

        crypto_access_token = self.cryptographer_access_token.crypto(access_token)

        await self.commitable.commit()

        return crypto_access_token
