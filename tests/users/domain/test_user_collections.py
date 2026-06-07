from modules.users.domain.collections import UserCollection
from modules.users.domain.entities import User


class TestUserCollection:
    def test_filter_by_username_returns_only_users_of_given_username(
        self, users: list[User]
    ):
        username = 'testuser1'
        expected = [user for user in users if user.username == username]

        collection = UserCollection(users)
        filtered = collection.filter_by_username(username)

        assert len(filtered) == len(expected)
        assert all(user.username == username for user in filtered)

    def test_filter_by_fullname_returns_only_users_with_given_fullname(
        self, users: list[User]
    ):
        fullname = 'Test User 1'
        expected = [user for user in users if user.fullname == fullname]

        collection = UserCollection(users)
        filtered = collection.filter_by_fullname(fullname)

        assert len(filtered) == len(expected)
        assert all(user.fullname == fullname for user in filtered)

    def test_filter_by_email_returns_only_users_with_given_email(
        self, users: list[User]
    ):
        email = 'testuser1@example.com'
        expected = [user for user in users if user.email == email]

        collection = UserCollection(users)
        filtered = collection.filter_by_email(email)

        assert len(filtered) == len(expected)
        assert all(user.email == email for user in filtered)

    def test_get_males_returns_only_males(self, users: list[User]):
        expected = [user for user in users if user.gender == 'male']

        collection = UserCollection(users)
        males = collection.get_males()

        assert len(males) == len(expected)
        assert all(user.gender == 'male' for user in males)

    def test_get_females_returns_only_females(self, users: list[User]):
        expected = [user for user in users if user.gender == 'female']

        collection = UserCollection(users)
        females = collection.get_females()

        assert len(females) == len(expected)
        assert all(user.gender == 'female' for user in females)

    def test_get_standard_users_returns_only_standard_users(self, users: list[User]):
        expected = [user for user in users if user.role == 'user']

        collection = UserCollection(users)
        standard_users = collection.get_standard_users()

        assert len(standard_users) == len(expected)
        assert all(user.role == 'user' for user in standard_users)

    def test_get_admin_users_returns_only_admins(self, users: list[User]):
        expected = [user for user in users if user.role == 'admin']

        collection = UserCollection(users)
        admins = collection.get_admin_users()

        assert len(admins) == len(expected)
        assert all(user.role == 'admin' for user in admins)
