from uuid import UUID

from odata_v4_query import ODataQueryOptions
from odata_v4_query.utils.sqlalchemy import apply_to_sqlalchemy_query
from pydantic import SecretStr
from sqlactive import DBConnection, execute

from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from modules.users.infrastructure.persistence.models.sqlite import (
    UserModel,
)


class SQLiteUserRepository(UserRepositoryABC):
    def __init__(self, conn: DBConnection) -> None:
        self._conn = conn
        self._session = conn.async_scoped_session

    async def get_by_id(self, id_: UUID) -> User | None:
        user = await UserModel.get(id_)
        return user.to_entity() if user else None

    async def all(self, odata_options: ODataQueryOptions) -> list[User]:
        query = apply_to_sqlalchemy_query(odata_options, UserModel)
        result = await execute(self._session, query)
        users = result.scalars().all()
        return [user.to_entity() for user in users]

    async def create(self, user: User, password: SecretStr) -> User:
        model = UserModel.from_entity(user, password)
        await model.save()
        return model.to_entity()

    async def update(self, user: User) -> User | None:
        model = await UserModel.get(user.id)
        if not model:
            return None

        model.username = user.username
        model.fullname = user.fullname
        model.email = user.email
        model.gender = user.gender
        await model.save()

        return model.to_entity()

    async def delete(self, id_: UUID) -> None:
        user = await UserModel.get(id_)
        if not user:
            return

        await user.delete()

    async def count(self, odata_options: ODataQueryOptions | None = None) -> int:
        if odata_options:
            query = apply_to_sqlalchemy_query(odata_options, UserModel)
            result = await execute(self._session, query)
            return result.scalar_one()

        return await UserModel.count()
