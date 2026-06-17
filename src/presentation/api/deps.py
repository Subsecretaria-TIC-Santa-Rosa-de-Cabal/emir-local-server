from typing import Generator
from sqlalchemy.orm import Session
from infrastructure.persistence.sqlalchemy.config import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
