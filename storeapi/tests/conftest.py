import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from storeapi.db.database import database
from storeapi.main import app

os.environ["ENV_STATE"] = "TEST"  # Enable asyncio debug mode for better error messages


@pytest.fixture(scope="session")
def anyio_backend():
    """
    This function is used by pytest to determine the backend for async tests.
    It returns 'asyncio' as the backend to be used.
    """
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    """
    Fixture to create a test client for the FastAPI application.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
async def reset_db() -> AsyncGenerator:
    """
    Fixture to reset the in-memory database before each test.
    This ensures that tests do not interfere with each other.
    """
    database.connect()
    yield
    database.disconnect()
    # No cleanup needed since we're using an in-memory dictionary


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    """
    Fixture to create an async test client for the FastAPI application.
    This can be used for testing async endpoints.
    """
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport, base_url=client.base_url
    ) as async_test_client:
        yield async_test_client
