from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from app.config.database import metadata
from modules.backoffice.service.domain import Service as BackofficeService

mapper_registry = registry()

service_table = Table(
    "service",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("name", String(100), nullable=False),
    Column("description", Text(), nullable=True),
    Column("price", DECIMAL(precision=9, scale=2), nullable=False),
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

mapper_registry.map_imperatively(BackofficeService, service_table, properties={
        '_id': service_table.c.id,
        '_name': service_table.c.name,
        '_description': service_table.c.description,
        '_price': service_table.c.price,
        '_is_active': service_table.c.is_active,
    })
