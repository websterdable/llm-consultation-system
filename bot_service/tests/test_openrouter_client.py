import pytest
import respx
from httpx import Response
from app.services.openrouter_client import OpenRouterClient

@pytest.mark.asyncio
async def test_chat_completion():
    mock_response = {
        "choices": [{"message": {"content": "Hello, world!"}}]
    }
    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(Response(200, json=mock_response))
        client = OpenRouterClient()
        result = await client.chat_completion([{"role": "user", "content": "Hi"}])
        assert result == "Hello, world!"