"""
api global dependency injection
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


@contextmanager
def get_database() -> Generator[Session, None, None]:
    """
    dependency inject database session to repositories
    :return: database session
    :rtype: Generator
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()