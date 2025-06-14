import logging

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse

from storeapi.db.database import comment_table, database, post_table
from storeapi.models.models import CommentIn, CommentOut, PostIn, PostOut
from storeapi.security.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=PostOut)
async def create_post(post: PostIn, current_user=Depends(get_current_user)):
    # Simulate creating a post and returning it with an ID
    logger.info(f"Creating post for user: {current_user}")
    new_post = {**post.model_dump(), "user_id": current_user["id"]}

    # In a real application, you would save this to a database
    # Here we just simulate it with an in-memory dictionary
    # post_id = len(posts) + 1
    # new_post = {"id": post_id, **new_post}
    # posts[post_id] = new_post

    query = post_table.insert().values(
        title=new_post["title"],
        content=new_post["content"],
        user_id=new_post["user_id"],
    )

    post_id = await database.execute(query)
    new_post["id"] = post_id

    return JSONResponse(content=new_post, status_code=status.HTTP_201_CREATED)


@router.get("/", response_model=list[PostOut])
async def list_posts():
    query = post_table.select()
    results = await database.fetch_all(query)
    return list(results)


async def find_post(post_id: int = Path(...)):
    query = post_table.select().where(post_table.c.id == post_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    return result


@router.delete("/{post_id}", response_model=dict)
async def delete_post(
    post_id: int, post=Depends(find_post), current_user=Depends(get_current_user)
):
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this post"
        )

    query = post_table.delete().where(post_table.c.id == post_id)
    await database.execute(query)
    return {"message": "Post deleted successfully"}


@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    post: PostIn,
    post_=Depends(find_post),
    current_user=Depends(get_current_user),
):
    if not post_:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post = post.model_dump()
    updated_post["id"] = post_id
    updated_post["user_id"] = current_user["id"]
    if post_["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this post"
        )

    query = (
        post_table.update()
        .where(post_table.c.id == post_id)
        .values(title=updated_post["title"], content=updated_post["content"])
    )
    await database.execute(query)
    return updated_post


# @router.patch("/{post_id}", response_model=PostOut)
# async def partial_update_post(post_id: int, post: PostIn):
#     if post_id not in posts:
#         raise HTTPException(status_code=404, detail="Post not found")

#     existing_post = posts[post_id]
#     updated_post = existing_post.copy()

#     # Update only the fields that are provided
#     for key, value in post.model_dump().items():
#         if value is not None:
#             updated_post[key] = value

#     posts[post_id] = updated_post

#     return updated_post


@router.post("/{post_id}/comments/", response_model=CommentOut)
async def add_comment(
    post_id: int,
    comment: CommentIn,
    post=Depends(find_post),
    current_user=Depends(get_current_user),
):
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    logger.info(f"Adding comment to post {post_id} by user {current_user['id']}")

    comment = {**comment.model_dump(), "user_id": current_user["id"]}
    query = comment_table.insert().values(
        post_id=post_id, content=comment["content"], user_id=comment["user_id"]
    )
    comment_id = await database.execute(query)

    comment = {"id": comment_id, **comment}

    return JSONResponse(content=comment, status_code=status.HTTP_201_CREATED)


@router.get("/{post_id}/comments/", response_model=list[CommentOut])
async def list_comments(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    results = await database.fetch_all(query)
    if not results:
        raise HTTPException(status_code=404, detail="Post/Comment not found")

    # Return all comments for the specified post
    return list(results)


@router.delete("/{post_id}/comments/{comment_id}", response_model=dict)
async def delete_comment(
    post_id: int,
    comment_id: int,
    posts=Depends(list_posts),
    post_comments=Depends(list_comments),
):
    if not any(post["id"] == post_id for post in posts):
        raise HTTPException(status_code=404, detail="Post not found")

    if not any(comment["id"] == comment_id for comment in post_comments):
        raise HTTPException(status_code=404, detail="Comment not found")

    query = comment_table.delete().where(
        (comment_table.c.post_id == post_id) & (comment_table.c.id == comment_id)
    )
    await database.execute(query)

    return {"message": "Comment deleted successfully"}


@router.get("/{post_id}")
async def get_post_with_comments(post_id: int, post=Depends(find_post)):
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post_comments = await list_comments(post_id)

    return {"post": post, "comments": post_comments}
