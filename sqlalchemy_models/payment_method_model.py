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

class PaymentMethodModel:

    id: UUID
    user_id: UUID
    name: str
    is_active: bool
    second_last_name: str | None
    created_at: datetime
    updated_at: datetime


payment_method_table = Table(
    "payment_method",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("name", String(100), nullable=True),
    Column("is_active", Boolean(), default=True),
    Column("created_at", DateTime(timezone=True), nullable=False, default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    ),
)

mapper_registry.map_imperatively(PaymentMethodModel, payment_method_table)
