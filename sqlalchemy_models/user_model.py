from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from app.config.database import metadata
from modules.backoffice.user.domain import User as BackofficeUser
from modules.app.user.domain import User as AppUser

mapper_registry = registry()

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

mapper_registry.map_imperatively(AppUser, user_table)

mapper_registry.map_imperatively(BackofficeUser, user_table, properties={
        '_User__id': user_table.c.id,
        '_User__username': user_table.c.username,
        '_User__password': user_table.c.password,
        '_User__is_active': user_table.c.is_active,
    })
