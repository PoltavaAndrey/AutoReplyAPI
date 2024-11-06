from typing import List
from app.database import newSession, PostOrm, CommentOrm
from sqlalchemy import select
from app.schemas import Post, Comment


class TaskRepository:
    @classmethod
    async def AddOnePost(cls, post: Post):
        async with newSession() as session:
            postDict = post.model_dump()

            post = PostOrm(**postDict)
            session.add(post)
            await session.flush()
            await session.commit()
            return post

    @classmethod
    async def FindAllPosts(cls) -> List[PostOrm]:
        async with newSession() as session:
            query = select(PostOrm)
            result = await session.execute(query)
            postModels = result.scalars().all()
            return postModels

    @classmethod
    async def AddOneComment(cls, comment: Comment):
        async with newSession() as session:
            commentDict = comment.model_dump()

            comment = CommentOrm(**commentDict)
            session.add(comment)
            await session.flush()
            await session.commit()
            return comment

    @classmethod
    async def FindAllComments(cls, postId: int) -> List[PostOrm]:
        async with newSession() as session:
            query = select(CommentOrm)  # .where(CommentOrm.post_id == postId)
            result = await session.execute(query)
            commentModels = result.scalars().all()
            return commentModels
