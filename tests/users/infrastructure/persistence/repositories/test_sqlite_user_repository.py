import pytest
from odata_v4_query import ODataQueryOptions

from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from modules.users.infrastructure.persistence.models.sqlite import (
    UserModel,
)
from shared.helpers.odata_helper import ODataHelper
from shared.utils.uuid_tools import uuid
from shared.utils.validation_types import HashedSecretStr


@pytest.mark.asyncio
class TestSQLiteUsersRepository:
    async def test_get_by_id_returns_user_when_user_exists(
        self, user_model: UserModel, users_repo: UserRepositoryABC
    ):
        user = await users_repo.get_by_id(user_model.id)

        assert user is not None
        assert user.username == user_model.username

    async def test_get_by_id_returns_none_when_user_does_not_exist(
        self, users_repo: UserRepositoryABC
    ):
        user = await users_repo.get_by_id(uuid())

        assert user is None

    async def test_all_returns_all_requested_users(
        self, user_models: list[UserModel], users_repo: UserRepositoryABC
    ):
        users = await users_repo.all(
            odata_options=ODataQueryOptions(top=10),
        )

        assert len(users) == len(user_models)
        assert users[0].username == user_models[0].username
        assert users[1].username == user_models[1].username

    async def test_create_returns_created_user(self, users_repo: UserRepositoryABC):
        await users_repo.create(
            User.Builder()
            .with_username('testuser1')
            .with_fullname('Test User 1')
            .with_email('testuser1@example.com')
            .with_gender('male')
            .build(),
            password=HashedSecretStr('password123'),
        )
        user = await UserModel.one()

        assert user.username == 'testuser1'
        assert user.fullname == 'Test User 1'
        assert user.email == 'testuser1@example.com'
        assert user.gender == 'male'
        assert user.created_at == user.updated_at

    async def test_update_returns_updated_user_when_user_exists(
        self, user_model: UserModel, users_repo: UserRepositoryABC
    ):
        user = await users_repo.update(
            User.Builder()
            .with_id(user_model.id)
            .with_username('updateduser')
            .with_fullname('Test User 1')
            .with_email('updateduser@example.com')
            .with_gender('female')
            .build(),
        )

        assert user is not None
        assert user.username == 'updateduser'
        assert user.fullname == user_model.fullname

    async def test_update_returns_none_when_user_does_not_exist(
        self, users_repo: UserRepositoryABC
    ):
        user = await users_repo.update(
            User.Builder()
            .with_username('nonexistentuser')
            .with_fullname('Nonexistent User')
            .with_email('nonexistentuser@example.com')
            .with_gender('male')
            .build(),
        )

        assert user is None

    async def test_delete_returns_none_when_user_exists(
        self, user_model: UserModel, users_repo: UserRepositoryABC
    ):
        deleted = await users_repo.delete(user_model.id)

        assert deleted is None
        assert await UserModel.count() == 0

    async def test_delete_returns_none_when_user_does_not_exist(
        self, users_repo: UserRepositoryABC
    ):
        deleted = await users_repo.delete(uuid())

        assert deleted is None

    async def test_count_returns_total_number_of_users(
        self, user_models: list[UserModel], users_repo: UserRepositoryABC
    ):
        count = await users_repo.count()

        assert count == len(user_models)

    @pytest.mark.usefixtures('user_models')
    async def test_count_returns_total_number_of_users_matching_query(
        self, users_repo: UserRepositoryABC
    ):
        odata_helper = ODataHelper.get_from_query(
            '$filter=gender eq "male"', max_top=100
        )

        count = await users_repo.count(odata_helper.get_for_counting())

        assert count == 1
