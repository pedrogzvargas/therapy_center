from uuid import UUID
from datetime import datetime
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from flask_app.config.database import metadata

mapper_registry = registry()


class PermissionModel:

    id: UUID
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

permission_table = Table(
    "permission",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("name", String(100), nullable=False),
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

mapper_registry.map_imperatively(PermissionModel, permission_table)
