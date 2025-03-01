from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenResponse:
    access_token: str
