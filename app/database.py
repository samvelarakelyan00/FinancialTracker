# SqlAlchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# Own modules
from core.settings import settings


engine = create_engine(
    url=settings.database_url
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_session() -> Session:
    session = Session()

    try:
        yield session
    except Exception as err:
        raise err
    finally:
        session.close()
