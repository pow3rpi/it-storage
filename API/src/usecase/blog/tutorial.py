from pydantic import StrBytes

from src.core.exceptions.blog import ContentNotFound
from src.dto.blog import TutorialDto
from src.dto.user import UserDto
from src.interface.repository.tutorial import TutorialStorageInterface
from src.schema.tutorial import CreateTutorialRequest, UpdateTutorialRequest, GetTutorialResponse


class TutorialUseCase:

    def __init__(self, repository: TutorialStorageInterface):
        self.repo = repository

    @staticmethod
    def _to_binary(file: str) -> StrBytes:
        file = ' '.join(format(ord(i), 'b') for i in file)
        file = bytes(file.encode('utf-8'))
        return file

    @staticmethod
    def _to_string(file: StrBytes) -> str:
        file = ''.join(chr(int(i, 2)) for i in file.decode('utf-8').split(' '))
        return file

    async def create_tutorial(self, user: UserDto, data: CreateTutorialRequest) -> TutorialDto:
        data.file = self._to_binary(data.file)
        tutorial = await self.repo.create_tutorial(
            user_id=user.id,
            title=data.title,
            file=data.file,
            tags=data.tags if data.tags else None
        )
        return tutorial

    async def get_tutorial(self, user: UserDto, post_id: int) -> GetTutorialResponse:
        tutorial = await self.repo.get_tutorial(user.id, post_id)
        if not tutorial:
            raise ContentNotFound()
        tutorial.file = self._to_string(tutorial.file)
        return GetTutorialResponse(title=tutorial.title, tags=tutorial.tags, file=tutorial.file)

    async def update_tutorial(self, user: UserDto, post_id: int, data: UpdateTutorialRequest) -> TutorialDto:
        data.file = self._to_binary(data.file)
        tutorial = await self.repo.update_tutorial(
            user_id=user.id,
            post_id=post_id,
            title=data.title,
            file=data.file,
            tags=data.tags if data.tags else None
        )
        if not tutorial:
            raise ContentNotFound()
        return tutorial
