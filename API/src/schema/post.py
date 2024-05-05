from __future__ import annotations
from typing import List

from pydantic import BaseModel, validator

from src.core import config
from src.core.enums import PostEnum
from src.core.exceptions.blog import InvalidTitle, InvalidTag, TooManyTags
from src.dto.blog import LinkDto, TutorialDto


class BasePost(BaseModel):
    title: str
    tags: List[str] | None

    @validator('title')
    def validate_title(cls, v):
        v = v.strip()
        if (
                len(v) < config.MIN_TITLE_LENGTH
                or len(v) > config.MAX_TITLE_LENGTH
        ):
            raise InvalidTitle()
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v:
            v = [tag.lower() for tag in v]
            v = list(set(v))
            if len(v) > config.MAX_N_TAGS:
                raise TooManyTags()
            for tag in v:
                if (
                        len(tag) < config.MIN_TAG_LENGTH
                        or len(tag) > config.MAX_TAG_LENGTH
                        or not all(i.isdigit()
                                   or i.isalpha()
                                   or i in config.TAG_ALLOWED_CHARS for i in tag)
                        or all(i in config.TAG_ALLOWED_CHARS for i in tag)
                ):
                    raise InvalidTag()
        return v


class DeletePostRequest(BaseModel):
    id: List[int]


class GetTagsResponse(BaseModel):
    tags: List[str]

    def to_dict(self):
        return {
            'tags': self.tags
        }


class GetPostsResponse(BaseModel):
    posts: List[LinkDto | TutorialDto]
    total: int

    def to_dict(self):
        items = []
        for post in self.posts:
            if isinstance(post, LinkDto):
                items.append({
                    'id': post.post_id,
                    'type': PostEnum.link.value,
                    'title': post.title,
                    'tags': post.tags,
                    'url': post.url,
                    'annotation': post.annotation
                })
            else:
                items.append({
                    'id': post.post_id,
                    'type': PostEnum.tutorial.value,
                    'title': post.title,
                    'tags': post.tags
                })
        return {
            'posts': items,
            'total': self.total
        }
