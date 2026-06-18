import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from infrastructure.persistence.sqlalchemy.config import Base


class FileModel(Base):
    __tablename__ = 'files'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    enabled = Column(
        Boolean,
        default=True,
        nullable=False
    )
    registration_date = Column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False
    )
    last_update = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )
    remote_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True
    )
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    route = Column(String, nullable=False)
    size = Column(BigInteger, nullable=False)
    hash = Column(String, nullable=False)
    hash_version = Column(String, nullable=False)
    observation = Column(String)

    created_by_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    created_by = relationship(
        "UserModel",
        back_populates="uploaded_files",
        foreign_keys=[created_by_id],
        remote_side="UserModel.id"
    )
