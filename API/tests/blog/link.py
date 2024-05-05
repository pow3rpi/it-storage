import sqlalchemy as sa

from pydantic import ValidationError

from src.adapter.sql_db.orm.blog import (
    tag_post_association_table, TagModel, LinkPostModel, BasePostModel
)
from src.core.exceptions.blog import (
    InvalidAnnotation, InvalidTitle, InvalidTag, ContentNotFound
)
from src.dto.blog import LinkDto
from src.schema.link import CreateLinkRequest, UpdateLinkRequest
from tests.base import BaseTest


class LinkTestCase(BaseTest):

    async def test_valid_creation(self):
        user = await self.valid_sign_up()
        link = await self.create_valid_link(user)
        async with self.db.session() as session:
            # check tags attached to the link post
            query = sa.select(tag_post_association_table) \
                .filter(tag_post_association_table.c.post_id == self.valid_post_id) \
                .order_by(tag_post_association_table.c.tag_id)
            associations = await session.execute(query)
            associations = associations.all()
            query = sa.select(TagModel) \
                .order_by(TagModel.id)
            tags = await session.execute(query)
            tags = tags.scalars().all()
            self.assertEqual(len(associations), len(link.tags) if link.tags else 0)
            for i in range(len(associations)):
                self.assertEqual(tags[i].id, associations[i].tag_id)
            if link.tags:
                self.assertEqual(sorted(link.tags), sorted([tag.name for tag in tags]))
            # check that link post has been created
            query = sa.select(LinkPostModel) \
                .filter(LinkPostModel.post_id == link.post_id,
                        LinkPostModel.url == link.url,
                        LinkPostModel.annotation == link.annotation)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)
            # check that base post has been created
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id == link.post_id,
                        BasePostModel.title == link.title)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)

    async def test_invalid_title(self):
        user = await self.valid_sign_up()
        for title in self.invalid_titles:
            with self.subTest(title):
                with self.assertRaises(InvalidTitle):
                    await self.link_use_case.create_link(
                        user,
                        CreateLinkRequest(
                            title=title, url=self.valid_url, annotation=self.valid_annotation, tags=self.valid_tags
                        )
                    )

    async def test_invalid_tag(self):
        user = await self.valid_sign_up()
        for tag in self.invalid_tags:
            with self.subTest(tag):
                with self.assertRaises(InvalidTag):
                    await self.link_use_case.create_link(
                        user,
                        CreateLinkRequest(
                            title=self.valid_title, url=self.valid_url, annotation=self.valid_annotation,
                            tags=self.valid_tags + [tag] if self.valid_tags else [tag]
                        )
                    )

    async def test_invalid_annotation(self):
        user = await self.valid_sign_up()
        with self.assertRaises(InvalidAnnotation):
            await self.link_use_case.create_link(
                user,
                CreateLinkRequest(
                    title=self.valid_title, url=self.valid_url, annotation=self.invalid_annotation, tags=self.valid_tags
                )
            )

    async def test_invalid_url(self):
        user = await self.valid_sign_up()
        for url in self.invalid_urls:
            with self.subTest(url):
                with self.assertRaises(ValidationError):
                    await self.link_use_case.create_link(
                        user,
                        CreateLinkRequest(
                            title=self.valid_title, url=url, annotation=self.valid_annotation, tags=self.valid_tags
                        )
                    )

    async def test_get_link(self):
        user = await self.valid_sign_up()
        link = await self.create_valid_link(user)
        result = await self.link_use_case.get_link(user, link.post_id)
        self.assertEqual(link.title, result.title)
        self.assertEqual(link.tags, result.tags)
        self.assertEqual(link.url, result.url)
        self.assertEqual(link.annotation, result.annotation)

    async def test_no_content_found(self):
        user = await self.valid_sign_up()
        link = await self.create_valid_link(user)
        with self.assertRaises(ContentNotFound):
            await self.link_use_case.get_link(user, link.post_id + 1)

    async def test_valid_update(self):
        user = await self.valid_sign_up()
        link = await self.create_valid_link(user)
        data = UpdateLinkRequest(
            title=self.valid_title_2, url=self.valid_url_2, annotation=self.valid_annotation_2, tags=self.valid_tags_2
        )
        result = await self.link_use_case.update_link(user, link.post_id, data)
        correct_result = LinkDto(
            post_id=link.post_id, title=data.title, url=data.url, annotation=data.annotation, tags=data.tags
        )
        self.assertEqual(result, correct_result)
        # check tags attached to the link post
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
            if link.tags:
                self.assertEqual(sorted(data.tags), sorted([tag.name for tag in tags]))
            # check that link post has been updated
            query = sa.select(LinkPostModel) \
                .filter(LinkPostModel.post_id == link.post_id,
                        LinkPostModel.url == data.url,
                        LinkPostModel.annotation == data.annotation)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)
            # check that base post has been updated
            query = sa.select(BasePostModel) \
                .filter(BasePostModel.id == link.post_id,
                        BasePostModel.title == data.title)
            res = await session.execute(query)
            res = res.scalar()
            self.assertIsNotNone(res)
