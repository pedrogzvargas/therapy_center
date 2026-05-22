from uuid import UUID
from datetime import datetime
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from flask_app.config.database import metadata

mapper_registry = registry()


class RolePermissionModel:

    id: UUID
    role_id: UUID
    permission_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

role_permission_table = Table(
    "role_permission",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("role_id", postgresql.UUID(as_uuid=True), ForeignKey("role.id", ondelete="RESTRICT"), nullable=False),
    Column("permission_id", postgresql.UUID(as_uuid=True), ForeignKey("permission.id", ondelete="RESTRICT"), nullable=False),
    Column("is_active", Boolean(), default=False, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    ),
)

mapper_registry.map_imperatively(RolePermissionModel, role_permission_table)
