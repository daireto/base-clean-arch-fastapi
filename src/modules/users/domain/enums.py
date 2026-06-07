from enum import StrEnum


class Gender(StrEnum):
    MALE = 'male'
    FEMALE = 'female'


class Role(StrEnum):
    USER = 'user'
    ADMIN = 'admin'
