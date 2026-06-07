from sqladmin import ModelView

from modules.users.infrastructure.persistence.models.sqlite import (
    UserModel,
)


class UserAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.username,
        UserModel.fullname,
        UserModel.email,
        UserModel.gender,
    ]
