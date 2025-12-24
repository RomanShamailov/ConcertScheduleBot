import os
import pytest
import aiohttp
from unittest.mock import AsyncMock


@pytest.fixture(autouse=True)
def set_bot_token_env():
    os.environ.setdefault("BOT_TOKEN", "TEST_TOKEN")


@pytest.fixture
def mock_session() -> aiohttp.ClientSession:
    session = AsyncMock(spec=aiohttp.ClientSession)
    return session
