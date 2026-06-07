import pytest

from modules.users.domain.entities import User


@pytest.fixture
def users() -> list[User]:
    return [
        User.Builder()
        .with_username('testuser1')
        .with_fullname('Test User 1')
        .with_email('testuser1@example.com')
        .with_gender('male')
        .with_role('user')
        .build(),
        User.Builder()
        .with_username('testuser2')
        .with_fullname('Test User 2')
        .with_email('testuser2@example.com')
        .with_gender('female')
        .with_role('user')
        .build(),
        User.Builder()
        .with_username('testuser3')
        .with_fullname('Test User 3')
        .with_email('testuser3@example.com')
        .with_gender('male')
        .with_role('user')
        .build(),
        User.Builder()
        .with_username('testuser4')
        .with_fullname('Test User 4')
        .with_email('testuser4@example.com')
        .with_gender('female')
        .with_role('admin')
        .build(),
        User.Builder()
        .with_username('testuser5')
        .with_fullname('Test User 5')
        .with_email('testuser5@example.com')
        .with_gender('male')
        .with_role('admin')
        .build(),
        User.Builder()
        .with_username('testuser6')
        .with_fullname('Test User 6')
        .with_email('testuser6@example.com')
        .with_gender('female')
        .with_role('admin')
        .build(),
    ]
