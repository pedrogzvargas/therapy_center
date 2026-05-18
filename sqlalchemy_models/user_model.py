from uuid import UUID
from datetime import datetime
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from flask_app.config.database import metadata

mapper_registry = registry()

class UserModel:

    id: UUID
    username: str
    password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

user_table = Table(
    "user",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("username", String(100), nullable=False, unique=True),
    Column("password", String(200), nullable=False),
    Column("is_active", Boolean(), default=True, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    ),
)

mapper_registry.map_imperatively(UserModel, user_table)
