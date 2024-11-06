import re
from typing import List
from fastapi import HTTPException, APIRouter
from app.repository import TaskRepository
from app.schemas import Post, Comment

bad_words = re.compile(r"\b(погане_слово1|погане_слово2)\b", re.IGNORECASE)

router = APIRouter()


@router.post("/posts/", response_model=Post)
async def create_post(post: Post):
    if bad_words.search(post.content) or bad_words.search(post.title):
        raise HTTPException(status_code=400, detail="Пост містить нецензурну лексику.")
    postId = await TaskRepository.AddOnePost(post)
    return postId


@router.get("/posts/", response_model=List[Post])
async def read_posts():
    return await TaskRepository.FindAllPosts()


@router.post("/comments/", response_model=Comment)
async def create_comment(comment: Comment):
    if bad_words.search(comment.content):
        raise HTTPException(status_code=400, detail="Коментар містить нецензурну лексику.")

    post_exists = False
    posts = await TaskRepository.FindAllPosts()
    for post in posts:
        if post.id == comment.post_id:
            post_exists = True
            break

    if not post_exists:
        raise HTTPException(status_code=404, detail="Пост не знайдено.")

    # comments.append(comment)
    commentId = await TaskRepository.AddOneComment(comment)
    return commentId


@router.get("/posts/{post_id}/comments", response_model=List[Comment])
async def read_comments(post_id: int):
    return await TaskRepository.FindAllComments(post_id)
