import sqlalchemy as sa

from src.adapter.sql_db.orm.blog import BasePostModel
from src.core.enums import SearchEnum
from src.schema.post import DeletePostRequest
from tests.base import BaseTest


class PostTestCase(BaseTest):

    async def test_valid_deletion(self):
        user = await self.valid_sign_up()
        link = await self.create_valid_link(user)
        tutorial = await self.create_valid_tutorial(user)
        await self.post_use_case.delete_post(user, DeletePostRequest(id=[link.post_id, tutorial.post_id]))
        async with self.db.session() as session:
            # check that base posts have been deleted
            query = sa.select(BasePostModel)
            posts = await session.execute(query)
            posts = posts.scalars().all()
            self.assertTrue(posts == [])
            # check that link posts have been deleted
            query = sa.select(BasePostModel)
            links = await session.execute(query)
            links = links.scalars().all()
            self.assertTrue(links == [])
            # check that tutorial posts have been deleted
            query = sa.select(BasePostModel)
            tutorials = await session.execute(query)
            tutorials = tutorials.scalars().all()
            self.assertTrue(tutorials == [])

    async def test_get_tags(self):
        await self.valid_sign_up()
        tags = await self.create_tags(['python', 'pytorch', 'machine-learning'])
        result = await self.post_use_case.get_tags('pyt')
        correct_result = tags[:2]
        self.assertEqual(result.tags, [tag.name for tag in correct_result])
        result = await self.post_use_case.get_tags('learn')
        correct_result = [tags[2]]
        self.assertEqual(result.tags, [tag.name for tag in correct_result])

    async def test_search(self):
        user = await self.valid_sign_up()
        link = await self.create_valid_link(user)
        tutorial = await self.create_valid_tutorial(user, second_post=True)
        # search scenario 1
        result = await self.post_use_case.get_posts(user, SearchEnum.all, None, 0)
        self.assertEqual(result.total, 2)
        self.assertEqual(sorted([post.post_id for post in result.posts]), [link.post_id, tutorial.post_id])
        # search scenario 2
        result = await self.post_use_case.get_posts(user, SearchEnum.link, None, 0)
        self.assertEqual(result.total, 1)
        self.assertEqual([post.post_id for post in result.posts], [link.post_id])
        # search scenario 3
        result = await self.post_use_case.get_posts(user, SearchEnum.tutorial, None, 0)
        self.assertEqual(result.total, 1)
        self.assertEqual([post.post_id for post in result.posts], [tutorial.post_id])
        # search scenario 4
        result = await self.post_use_case.get_posts(user, SearchEnum.all, self.valid_tags[:9], 0)
        self.assertEqual(result.total, 2)
        self.assertEqual([post.post_id for post in result.posts], [link.post_id, tutorial.post_id])
        # search scenario 5
        result = await self.post_use_case.get_posts(user, SearchEnum.all, self.valid_tags_2, 0)
        self.assertEqual(result.total, 2)
        self.assertEqual([post.post_id for post in result.posts], [tutorial.post_id, link.post_id])
        # search scenario 6
        result = await self.post_use_case.get_posts(user, SearchEnum.all, [self.valid_tags[-1]], 0)
        self.assertEqual(result.total, 1)
        self.assertEqual([post.post_id for post in result.posts], [link.post_id])
