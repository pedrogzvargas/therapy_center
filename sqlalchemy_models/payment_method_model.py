from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from app.config.database import metadata
from modules.app.payment_method.domain import PaymentMethod as AppPaymentMethod
from modules.backoffice.payment_method.domain import PaymentMethod as BackofficePaymentMethod

mapper_registry = registry()

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

mapper_registry.map_imperatively(AppPaymentMethod, payment_method_table)
mapper_registry.map_imperatively(BackofficePaymentMethod, payment_method_table, properties={
        '_PaymentMethod__id': payment_method_table.c.id,
        '_PaymentMethod__name': payment_method_table.c.name,
        '_PaymentMethod__is_active': payment_method_table.c.is_active,
    })
