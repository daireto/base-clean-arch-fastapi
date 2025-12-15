from sqladmin import ModelView

from modules.resources.infrastructure.persistence.models.sqlite import ResourceModel


class ResourceAdmin(ModelView, model=ResourceModel):
    column_list = [
        ResourceModel.name,
        ResourceModel.url,
        ResourceModel.type,
    ]
