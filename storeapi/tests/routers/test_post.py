import pytest
from httpx import AsyncClient


def create_post(body: dict, async_client: AsyncClient) -> dict:
    """
    Helper function to create a post using the async client.
    """
    response = async_client.post("/posts/", json=body)
    assert response.status_code == 200, f"Failed to create post: {response.text}"
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    """
    Fixture to create a post before each test.
    This ensures that tests have a post to work with.
    """
    return await create_post(
        {"title": "Test post", "content": "Test post Content"}, async_client
    )


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    """
    Fixture to create a post for testing.
    This can be used in tests that require a post to be present.
    """
    post = await async_client.post(
        "/posts/",
        json={
            "title": "Test post",
            "content": "Test post Content",
            "name": "Test User",
        },
    )

    assert post.status_code == 201, f"Failed to create post: {post.text}"
    assert {
        "id": 1,
        "title": "Test post",
        "content": "Test post Content",
    }.items() <= post.json().items(), "Post creation response mismatch"
