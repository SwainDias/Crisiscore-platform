"""
tests/conftest.py
Shared pytest fixtures for all tests.
Uses an in-memory / test MongoDB database via mongomock-motor (or a real
test DB configured via TEST_MONGO_URI env var).
"""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app.main import create_app


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest_asyncio.fixture(scope="function")
async def app() -> FastAPI:
    """Creates a fresh FastAPI app per test function."""
    return create_app()


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client wired to the test app (no real network)."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
