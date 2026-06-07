from typing import Self

from pydantic import EmailStr, Field

from modules.users.domain.enums import Gender
from shared.domain.bases.entity import Entity


class User(Entity):
    username: str = Field(min_length=5, max_length=15)
    fullname: str = Field(min_length=5, max_length=50)
    email: EmailStr
    gender: Gender

    class Builder(Entity.Builder):
        def __init__(self) -> None:
            super().__init__()
            self._username = None
            self._fullname = None
            self._email = None
            self._gender = None

        def with_username(self, username: str) -> Self:
            self._username = username
            return self

        def with_fullname(self, fullname: str) -> Self:
            self._fullname = fullname
            return self

        def with_email(self, email: EmailStr) -> Self:
            self._email = email
            return self

        def with_gender(self, gender: Gender | str) -> Self:
            self._gender = gender
            return self

        def build(self) -> 'User':
            return User.model_validate(
                {
                    'id': self._id,
                    'username': self._username,
                    'fullname': self._fullname,
                    'email': self._email,
                    'gender': self._gender,
                }
            )
