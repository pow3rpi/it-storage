from typing import List

from src.core.enums import SearchEnum
from src.dto.user import UserDto
from src.interface.repository.post import PostStorageInterface
from src.schema.post import DeletePostRequest, GetPostsResponse, GetTagsResponse


class PostUseCase:

    def __init__(self, repository: PostStorageInterface):
        self.repo = repository

    async def get_tags(self, string: str) -> GetTagsResponse:
        tags = await self.repo.get_tags(string=string)
        if not tags:
            tags = []
        tags = [tag.name for tag in tags]
        return GetTagsResponse(tags=tags)

    async def get_posts(self, user: UserDto, search_type: SearchEnum,
                        search_filter: List[str] | str | None, page: int) -> GetPostsResponse:
        # check search type/filter
        if isinstance(search_filter, str):
            posts, n_posts = await self.repo.get_posts_by_title(
                user_id=user.id,
                string=search_filter,
                search_type=search_type,
                offset=page,
            )
        elif isinstance(search_filter, List):
            posts, n_posts = await self.repo.get_posts_by_tags(
                user_id=user.id,
                tags=search_filter,
                search_type=search_type,
                offset=page,
            )
        else:
            posts, n_posts = await self.repo.get_posts(
                user_id=user.id,
                search_type=search_type,
                offset=page,
            )
        return GetPostsResponse(
            posts=posts,
            total=n_posts
        )

    async def delete_post(self, user: UserDto, data: DeletePostRequest):
        await self.repo.delete_post(
            user_id=user.id,
            post_id=data.id
        )
