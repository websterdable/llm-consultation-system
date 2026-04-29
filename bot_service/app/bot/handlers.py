import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()


@router.message(Command("token"))
async def token_handler(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /token <JWT>")
        return
    token = parts[1]
    try:
        decode_and_validate(token)
        redis = await get_redis()
        await redis.set(f"token:{message.from_user.id}", token)
        await message.answer("Токен сохранён. Теперь можно отправлять запросы модели.")
    except ValueError:
        await message.answer("Неверный или истёкший токен. Получите новый токен через Auth Service.")


@router.message()
async def text_handler(message: Message):
    redis = await get_redis()
    token = await redis.get(f"token:{message.from_user.id}")
    if not token:
        await message.answer("Сначала отправьте токен командой: /token <JWT>")
        return
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("Токен недействителен. Получите новый токен через Auth Service.")
        return

    await message.answer("Запрос принят. Ответ придёт следующим сообщением.")
    llm_request.delay(message.chat.id, message.text)

    # Ждём ответ в Redis
    for _ in range(30):
        await asyncio.sleep(2)
        answer = await redis.get(f"answer:{message.chat.id}")
        if answer:
            await message.answer(answer)
            await redis.delete(f"answer:{message.chat.id}")
            return