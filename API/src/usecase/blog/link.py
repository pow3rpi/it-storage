from src.core.exceptions.blog import ContentNotFound
from src.dto.blog import LinkDto
from src.dto.user import UserDto
from src.interface.repository.link import LinkStorageInterface
from src.schema.link import CreateLinkRequest, UpdateLinkRequest, GetLinkResponse


class LinkUseCase:

    def __init__(self, repository: LinkStorageInterface):
        self.repo = repository

    async def create_link(self, user: UserDto, data: CreateLinkRequest) -> LinkDto:
        link = await self.repo.create_link(
            user_id=user.id,
            title=data.title,
            url=data.url,
            annotation=data.annotation,
            tags=data.tags if data.tags else None
        )
        return link

    async def get_link(self, user: UserDto, post_id: int) -> GetLinkResponse:
        link = await self.repo.get_link(user.id, post_id)
        if not link:
            raise ContentNotFound()
        return GetLinkResponse(title=link.title, tags=link.tags, url=link.url, annotation=link.annotation)

    async def update_link(self, user: UserDto, post_id: int, data: UpdateLinkRequest) -> LinkDto:
        link = await self.repo.update_link(
            user_id=user.id,
            post_id=post_id,
            title=data.title,
            url=data.url,
            annotation=data.annotation,
            tags=data.tags if data.tags else None
        )
        if not link:
            raise ContentNotFound()
        return link
