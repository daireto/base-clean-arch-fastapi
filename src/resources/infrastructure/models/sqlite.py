from uuid import UUID, uuid4

from sqlactive import ActiveRecordBaseModel
from sqlalchemy.orm import Mapped, mapped_column


class SQLiteDBModel(ActiveRecordBaseModel):
    __abstract__ = True


class SQLiteResourceModel(SQLiteDBModel):
    __tablename__ = 'resources'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
