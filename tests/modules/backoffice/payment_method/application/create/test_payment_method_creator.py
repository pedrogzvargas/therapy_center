from uuid import UUID
from unittest.mock import MagicMock
from modules.backoffice.payment_method.application.create import PaymentMethodCreator
from modules.shared.bus.event.infraestructure.fake import FakeEventBus
from modules.backoffice.payment_method.infrastructure.repositories.postgres import PostgresPaymentMethodRepository

from sqlalchemy.orm import Session
from sqlalchemy.orm import configure_mappers


def test_payment_method_creator():
    configure_mappers()
    mock_session = MagicMock(spec=Session)
    mock_session.get.return_value = None
    mock_session.__enter__.return_value = mock_session
    payment_method_repository = PostgresPaymentMethodRepository(session=mock_session)
    payment_method_creator = PaymentMethodCreator(
        payment_method_repository=payment_method_repository,
        event_bus=FakeEventBus(),
    )
    payment_method_creator(
        payment_method_id=UUID("76033fcb-28be-4929-9380-3b79f8617b98"),
        name="Tarjeta de Crédito",
        is_active=True,
    )
    pass
