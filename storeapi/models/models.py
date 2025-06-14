from pydantic import BaseModel, ConfigDict


# Define the Post model for input and output
# This model will be used for both creating and retrieving posts
class PostIn(BaseModel):
    title: str
    content: str


class PostOut(PostIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int


class CommentIn(BaseModel):
    post_id: int
    content: str


class CommentOut(CommentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int


class User(BaseModel):
    username: str
    email: str
    password: str


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(UserIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
