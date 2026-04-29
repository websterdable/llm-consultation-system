import asyncio

from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient
from app.infra.redis import get_redis


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> str:
    async def _run():
        client = OpenRouterClient()
        messages = [
            {"role": "system", "content": "Ты — полезный ассистент. Отвечай кратко, по делу, не более 3-4 предложений."},
            {"role": "user", "content": prompt},
        ]
        answer = await client.chat_completion(messages)
        redis = await get_redis()
        await redis.set(f"answer:{tg_chat_id}", answer)
        return answer

    return asyncio.run(_run())