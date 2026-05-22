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


class UserRoleModel:

    id: UUID
    user_id: UUID
    role_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

user_role_table = Table(
    "user_role",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("user_id", postgresql.UUID(as_uuid=True), ForeignKey("user.id", ondelete="RESTRICT"), nullable=False),
    Column("role_id", postgresql.UUID(as_uuid=True), ForeignKey("role.id", ondelete="RESTRICT"), nullable=False),
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

mapper_registry.map_imperatively(UserRoleModel, user_role_table)
