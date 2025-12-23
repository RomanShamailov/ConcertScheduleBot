import pytest
import aiohttp
from unittest.mock import AsyncMock


@pytest.fixture
def mock_session() -> aiohttp.ClientSession:
    session = AsyncMock(spec=aiohttp.ClientSession)
    return session
