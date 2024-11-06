from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class Comment(BaseModel):
    post_id: int
    content: str


class User(BaseModel):
    username: str
    email: str
    password_hash: str
