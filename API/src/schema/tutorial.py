from __future__ import annotations
from typing import List

from pydantic import BaseModel, validator

from src.core import config
from src.core.exceptions.blog import InvalidFileSize
from src.schema.post import BasePost


class CreateTutorialRequest(BasePost):
    file: str

    @validator('file')
    def validate_file(cls, v):
        file_size = len(v.encode('utf-8'))
        if file_size > config.MAX_TUTORIAL_SIZE:
            raise InvalidFileSize()
        return v


class UpdateTutorialRequest(CreateTutorialRequest):
    pass


class GetTutorialResponse(BaseModel):
    title: str
    tags: List[str] | None
    file: str

    def to_dict(self):
        return {
            'title': self.title,
            'tags': self.tags,
            'file': self.file
        }
