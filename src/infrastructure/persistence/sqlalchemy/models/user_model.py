import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from infrastructure.persistence.sqlalchemy.config import Base


class UserModel(Base):
    __tablename__ = 'users'

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
        unique=True,
        nullable=False
    )
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    id_number = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    email = Column(String, unique=True)

    uploaded_files = relationship(
        "FileModel",
        back_populates="created_by",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="[FileModel.created_by_id]",
        primaryjoin="UserModel.id==FileModel.created_by_id"
    )
