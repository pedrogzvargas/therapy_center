from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from app.config.database import metadata
from modules.backoffice.customer.domain import Customer as BackofficeCustomer

mapper_registry = registry()

customer_table = Table(
    "customer",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("user_id", postgresql.UUID(as_uuid=True), ForeignKey("user.id", ondelete="RESTRICT"), nullable=False),
    Column("name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("second_last_name", String(100), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False, default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    ),
)

mapper_registry.map_imperatively(BackofficeCustomer, customer_table)
