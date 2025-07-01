from uuid import UUID

from sqlactive import ActiveRecordBaseModel
from sqlalchemy.orm import Mapped, mapped_column


class DBModel(ActiveRecordBaseModel):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True)


class SQLiteResourceModel(DBModel):
    __tablename__ = 'resources'

    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
