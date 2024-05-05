import sqlalchemy as sa

from src.adapter.sql_db.orm.blog import (
    tag_post_association_table, TagModel, TutorialPostModel, BasePostModel
)
from src.core.exceptions.blog import InvalidTitle, InvalidTag, ContentNotFound
from src.dto.blog import TutorialDto
from src.schema.tutorial import CreateTutorialRequest, UpdateTutorialRequest
from tests.base import BaseTest


class TutorialTestCase(BaseTest):

    async def test_valid_creation(self):
        user = await self.valid_sign_up()
        tutorial = await self.create_valid_tutorial(user)
        async with self.db.session() as session:
            # check tags attached to the tutorial post
            query = sa.select(tag_post_association_table) \
                .filter(tag_post_association_table.c.post_id == self.valid_post_id) \
                .order_by(tag_post_association_table.c.tag_id)
            associations = await session.execute(query)
            associations = associations.all()
            query = sa.select(TagModel) \
                .order_by(TagModel.id)
            tags = await session.execute(query)
            tags = tags.scalars().all()
            self.assertEqual(len(associations), len(tutorial.tags) if tutorial.tags else 0)
            for i in range(len(associations)):
                self.assertEqual(tags[i].id, associations[i].tag_id)
            if tutorial.tags:
                self.assertEqual(sorted(tutorial.tags), sorted([tag.name for tag in tags]))
            # check that tutorial post has been created
            query = sa.select(TutorialPostModel) \
                .filter(TutorialPostModel.post_id == tutorial.post_id,
                        TutorialPostModel.file == tutorial.file)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)
            # check that base post has been created
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id == tutorial.post_id,
                        BasePostModel.title == tutorial.title)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)

    async def test_invalid_title(self):
        user = await self.valid_sign_up()
        for title in self.invalid_titles:
            with self.subTest(title):
                with self.assertRaises(InvalidTitle):
                    await self.tutorial_use_case.create_tutorial(
                        user,
                        CreateTutorialRequest(title=title, file=self.valid_file, tags=self.valid_tags)
                    )

    async def test_invalid_tag(self):
        user = await self.valid_sign_up()
        for tag in self.invalid_tags:
            with self.subTest(tag):
                with self.assertRaises(InvalidTag):
                    await self.tutorial_use_case.create_tutorial(
                        user,
                        CreateTutorialRequest(
                            title=self.valid_title, file=self.valid_file,
                            tags=self.valid_tags + [tag] if self.valid_tags else [tag]
                        )
                    )

    async def test_get_tutorial(self):
        user = await self.valid_sign_up()
        tutorial = await self.create_valid_tutorial(user)
        result = await self.tutorial_use_case.get_tutorial(user, tutorial.post_id)
        self.assertEqual(tutorial.title, result.title)
        self.assertEqual(tutorial.tags, result.tags)
        self.assertEqual(self.tutorial_use_case._to_string(tutorial.file), result.file)

    async def test_no_content_found(self):
        user = await self.valid_sign_up()
        tutorial = await self.create_valid_tutorial(user)
        with self.assertRaises(ContentNotFound):
            await self.tutorial_use_case.get_tutorial(user, tutorial.post_id + 1)

    async def test_valid_update(self):
        user = await self.valid_sign_up()
        tutorial = await self.create_valid_tutorial(user)
        data = UpdateTutorialRequest(title=self.valid_title_2, file=self.valid_file_2, tags=self.valid_tags_2)
        binary_file = self.tutorial_use_case._to_binary(data.file)
        result = await self.tutorial_use_case.update_tutorial(user, tutorial.post_id, data)
        correct_result = TutorialDto(post_id=tutorial.post_id, title=data.title, file=binary_file, tags=data.tags)
        self.assertEqual(result, correct_result)
        # check tags attached to the tutorial post
        async with self.db.session() as session:
            query = sa.select(tag_post_association_table) \
                .filter(tag_post_association_table.c.post_id == self.valid_post_id) \
                .order_by(tag_post_association_table.c.tag_id)
            associations = await session.execute(query)
            associations = associations.all()
            query = sa.select(TagModel) \
                .filter(TagModel.id.in_([tag.id for tag in associations]))
            tags = await session.execute(query)
            tags = tags.scalars().all()
            self.assertEqual(len(associations), len(data.tags) if data.tags else 0)
            if tutorial.tags:
                self.assertEqual(sorted(data.tags), sorted([tag.name for tag in tags]))
            # check that tutorial post has been updated
            query = sa.select(TutorialPostModel) \
                .filter(TutorialPostModel.post_id == tutorial.post_id,
                        TutorialPostModel.file == binary_file)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)
            # check that base post has been updated
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id == tutorial.post_id,
                        BasePostModel.title == data.title)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)
