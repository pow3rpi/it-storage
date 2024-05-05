from dataclasses import dataclass
from typing import List

from pydantic import AnyHttpUrl, StrBytes


@dataclass
class TagDto:
    id: int
    name: str


@dataclass
class LinkDto:
    post_id: int
    title: str
    url: AnyHttpUrl
    annotation: str | None
    tags: List[str] | None


@dataclass
class TutorialDto:
    post_id: int
    title: str
    file: StrBytes | str
    tags: List[str] | None
