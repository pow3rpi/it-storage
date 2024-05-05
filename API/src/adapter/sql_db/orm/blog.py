from sqlalchemy import (
    Column, ForeignKey, Table, String,
    Integer, DateTime, LargeBinary
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

from src.adapter.sql_db.base import Base
from src.core import config
from src.core.enums import PostEnum

tag_post_association_table = Table(
    'tag_post_association',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tag_id', ForeignKey('tag.id')),
    Column('post_id', ForeignKey('base_post.id', ondelete='CASCADE'))
)


class TagModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=config.MAX_TAG_LENGTH), nullable=False)

    post = relationship('BasePostModel', secondary=tag_post_association_table, back_populates='tag')

    __tablename__ = 'tag'
    __mapper_args__ = {
        'polymorphic_identity': 'tag'
    }


class BasePostModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str]
    title = Column(String(length=config.MAX_TITLE_LENGTH), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    creation_time = Column(DateTime, server_default=func.now())

    author = relationship('UserModel', back_populates='post')
    tag = relationship('TagModel', secondary=tag_post_association_table, back_populates='post', passive_deletes=True)
    link_post = relationship('LinkPostModel', back_populates='base_post', passive_deletes=True)
    tutorial_post = relationship('TutorialPostModel', back_populates='base_post', passive_deletes=True)

    __tablename__ = 'base_post'
    __mapper_args__ = {
        'polymorphic_identity': 'base_post',
        'polymorphic_on': 'type'
    }

    def __repr__(self):
        return f'{self.__class__.__name__}'


class LinkPostModel(BasePostModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('base_post.id', ondelete='CASCADE'))
    url = Column(String, nullable=False)
    annotation = Column(String(length=config.MAX_ANNOTATION_LENGTH), nullable=True)

    base_post = relationship('BasePostModel', back_populates='link_post')

    __tablename__ = 'link_post'
    __mapper_args__ = {
        'polymorphic_identity': PostEnum.link.value
    }


class TutorialPostModel(BasePostModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('base_post.id', ondelete='CASCADE'))
    file = Column(LargeBinary(length=config.MAX_TUTORIAL_SIZE), nullable=False)

    base_post = relationship('BasePostModel', back_populates='tutorial_post')

    __tablename__ = 'tutorial_post'
    __mapper_args__ = {
        'polymorphic_identity': PostEnum.tutorial.value
    }
