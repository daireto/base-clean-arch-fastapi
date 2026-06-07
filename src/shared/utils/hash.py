import bcrypt
from pydantic import SecretStr


def encrypt_secret(secret: str | SecretStr) -> str:
    if isinstance(secret, SecretStr):
        secret = secret.get_secret_value()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(secret.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_secret(secret: str | SecretStr, hashed: str) -> bool:
    if isinstance(secret, SecretStr):
        secret = secret.get_secret_value()

    return bcrypt.checkpw(secret.encode('utf-8'), hashed.encode('utf-8'))
