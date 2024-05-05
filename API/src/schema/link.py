from __future__ import annotations
from typing import List

from pydantic import BaseModel, AnyHttpUrl, validator

from src.core import config
from src.core.exceptions.blog import InvalidAnnotation
from src.schema.post import BasePost


class CreateLinkRequest(BasePost):
    url: AnyHttpUrl
    annotation: str | None

    @validator('annotation')
    def validate_annotation(cls, v):
        if v:
            v = v.strip()
            if len(v) > config.MAX_ANNOTATION_LENGTH:
                raise InvalidAnnotation()
        return v


class UpdateLinkRequest(CreateLinkRequest):
    pass


class GetLinkResponse(BaseModel):
    title: str
    tags: List[str] | None
    url: AnyHttpUrl
    annotation: str | None

    def to_dict(self):
        return {
            'title': self.title,
            'tags': self.tags,
            'url': self.url,
            'annotation': self.annotation
        }
