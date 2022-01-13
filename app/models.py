import uuid
from datetime import datetime

import ormar

from .database import database, metadata


class CoreModel(ormar.Model):
    pk: int = ormar.Integer(primary_key=True)
    id: uuid.UUID = ormar.UUID(default=uuid.uuid4)
    created_at: datetime = ormar.DateTime(default=datetime.now)
    updated_at: datetime = ormar.DateTime(default=datetime.now)
    is_active: bool = ormar.Boolean(default=True)

    class Meta:
        abstract = True
        metadata = metadata
        database = database


class Book(CoreModel):
    title: str = ormar.String(max_length=150)
    description: str = ormar.Text(nullable=True)
    price: int = ormar.Integer()

    class Meta(ormar.ModelMeta):
        tablename = "books"
