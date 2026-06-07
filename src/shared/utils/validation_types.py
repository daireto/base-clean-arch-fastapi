from pydantic import SecretStr

from shared.utils.hash import encrypt_secret


class HashedSecretStr(SecretStr):
    def get_secret_value(self) -> str:
        value = super().get_secret_value()
        return encrypt_secret(value)
