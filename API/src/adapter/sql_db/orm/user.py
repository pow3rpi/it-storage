import uuid

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType

from src.adapter.sql_db.base import Base
from src.adapter.sql_db.orm.blog import BasePostModel
from src.core import config


class UserModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=config.MAX_USERNAME_LENGTH), unique=True, nullable=False)
    first_name = Column(String(length=config.MAX_NAME_LENGTH))
    last_name = Column(String(length=config.MAX_NAME_LENGTH))
    email = Column(EmailType, unique=True, nullable=False)
    password = Column(String(length=200), nullable=False)
    is_active = Column(Boolean, default=False)

    post = relationship(BasePostModel, back_populates='author')
    verification = relationship('SignUpVerificationModel', back_populates='user', passive_deletes=True)

    __tablename__ = 'user'


class SignUpVerificationModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    token = Column(UUID(as_uuid=True), default=uuid.uuid4)
    creation_time = Column(DateTime, server_default=func.now())
    is_used = Column(Boolean, default=False)

    user = relationship('UserModel', back_populates='verification')

    __tablename__ = 'sign_up_verification'
