from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from venue_vendue.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@contextmanager
def get_session():
    """
    A session context manager.

    Example usage:

    with get_session() as session:
        ...

    NOTE: You don't need this session context manager if you are using
    the SessionMeta meta class.
    """
    try:
        session = Session()
        yield session
    except Exception:
        session.rollback()
        raise
    else:
        if settings.TESTING:
            session.flush()
        else:
            session.commit()
    finally:
        if not settings.TESTING:
            Session.remove()
