from modules.users.domain.entities import User
from shared.domain.bases.collection import Collection


class UserCollection(Collection[User]):
    def __init__(
        self,
        users: list[User],
        total_stored: int | None = None,
    ) -> None:
        super().__init__(users)
        self.total_stored = total_stored or len(users)

    def filter_by_username(self, username: str) -> 'UserCollection':
        return UserCollection([user for user in self if user.username == username])

    def filter_by_fullname(self, fullname: str) -> 'UserCollection':
        return UserCollection(
            [user for user in self if fullname.lower() in user.fullname.lower()]
        )

    def filter_by_email(self, email: str) -> 'UserCollection':
        return UserCollection([user for user in self if user.email == email])

    def filter_by_gender(self, gender: str) -> 'UserCollection':
        return UserCollection([user for user in self if user.gender == gender])

    def get_males(self) -> 'UserCollection':
        return self.filter_by_gender('male')

    def get_females(self) -> 'UserCollection':
        return self.filter_by_gender('female')

    def sort_by_username(self) -> 'UserCollection':
        return UserCollection(sorted(self, key=lambda user: user.username))
