from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator

async def get_session():
    environ = PyEnviron()
    db_values = dict(
        dialect=environ.get_str("POSTGRES_DIALECT"),
        driver=environ.get_str("POSTGRES_DRIVER"),
        host=environ.get_str("POSTGRES_HOST"),
        user=environ.get_str("POSTGRES_USER"),
        password=environ.get_str("POSTGRES_PASSWORD"),
        port=environ.get_str("POSTGRES_PORT"),
        db=environ.get_str("POSTGRES_DB"),
        echo=environ.get_bool("SQL_ECHO", False),
    )

    async with AsyncAlchemySessionCreator(**db_values).get_session() as session:
        yield session
