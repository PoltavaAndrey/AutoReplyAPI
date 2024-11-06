from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine(
    "sqlite+aiosqlite:///posts.db"
)
newSession = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class PostOrm(Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[Optional[str]]
    published: Mapped[Optional[bool]]

    comments: Mapped[List["CommentOrm"]] = relationship(back_populates="post")


class CommentOrm(Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    content: Mapped[Optional[str]]

    post: Mapped["PostOrm"] = relationship(back_populates="comments")


async def CreateTables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def DeleteTables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
