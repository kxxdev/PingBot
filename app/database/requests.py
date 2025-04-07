from sqlalchemy import select, update
from app.database.models import Chat, async_session


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def get_chat(session, chat_tg_id: int) -> Chat:
    return await session.scalar(
        select(Chat)
        .where(Chat.tg_id == chat_tg_id)
    )


async def set_chat(chat_tg_id: int) -> Chat:
    chat = await get_chat(chat_tg_id=chat_tg_id)
    if not chat:
        async with async_session() as session:
            session.add(Chat(tg_id=chat_tg_id))
            await session.commit()
            return await get_chat(chat_tg_id=chat_tg_id)
    return chat


@connection
async def add_user_to_chat(session, chat_tg_id: int, user_tg_id: int) -> Chat:
    chat = await set_chat(chat_tg_id=chat_tg_id)
    if user_tg_id not in chat.users_tg_ids:
        chat.users_tg_ids.append(user_tg_id)
        await session.execute(
            update(Chat)
            .where(Chat.tg_id == chat_tg_id)
            .values(users_tg_ids=chat.users_tg_ids)
        )
        await session.commit()


@connection
async def remove_user_from_chat(session, chat_tg_id: int, user_tg_id: int) -> Chat:
    chat = await set_chat(chat_tg_id=chat_tg_id)
    if user_tg_id in chat.users_tg_ids:
        chat.users_tg_ids.remove(user_tg_id)
        await session.execute(
            update(Chat)
            .where(Chat.tg_id == chat_tg_id)
            .values(users_tg_ids=chat.users_tg_ids)
        )
        await session.commit()
