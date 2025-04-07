import os
from pydub import AudioSegment
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message

from app.database.requests import add_user_to_chat, remove_user_from_chat, set_chat
from app.generators import gpt_voice_to_text

chat = Router()


@chat.message(F.text.lower().in_(['@all', 'кто в доту']))
async def mention_all_users(message: Message):
    chat_tg_id = int(message.chat.id)
    author = message.from_user
    author_tg_id = int(author.id)
    if not str(chat_tg_id).startswith('-'):
        return
    await add_user_to_chat(chat_tg_id=chat_tg_id, user_tg_id=author_tg_id)
    chat = await set_chat(chat_tg_id=chat_tg_id)

    pins = []
    for user_tg_id in chat.users_tg_ids:
        chat_member = await message.bot.get_chat_member(chat_id=chat_tg_id, user_id=user_tg_id)
        if not chat_member or chat_member.status == 'left' or chat_member.user.is_bot:
            await remove_user_from_chat(chat_tg_id=chat_tg_id, user_tg_id=user_tg_id)
        elif author_tg_id != user_tg_id:
            # pins.append(f'[👤](tg://user?id={chat_member.user.id})')
            pins.append(f'<a href="tg://user?id={chat_member.user.id}">🤡</a>')

    if len(pins) >= 10:
        await message.answer(
            text=f'Я не могу упомянуть больше 10 человек. Ваш чат не подходит для меня. Всего хорошего (идите нахуй).'
        )
        return await message.bot.leave_chat(chat_id=chat_tg_id)
    if len(pins) == 0:
        return await message.answer(
            text=f'Я упоминаю только тех, кто писал в чат с момента моего прибытия. Кроме тебя и тут никого не вижу (долбаеб)'
        )

    await message.answer(
        text=f'<b>{author.full_name} решил собрать вас всех!</b>\n\nКлоуны {" ".join(pins)}, вас ожидают',
        parse_mode='HTML'
    )


@chat.message(F.content_type == 'voice')
async def voice_to_text(message: Message):
    Path('voices').mkdir(parents=True, exist_ok=True)

    voice_file = await message.bot.get_file(file_id=message.voice.file_id)
    voice_path = f'voices/voice-{message.voice.file_unique_id}'

    await message.bot.download_file(file_path=voice_file.file_path, destination=f'{voice_path}.ogg')

    voice_ogg = AudioSegment.from_file(f'{voice_path}.ogg', format='ogg')
    voice_ogg.export(
        f'{voice_path}.mp3', format='mp3'
    )

    os.remove(f'{voice_path}.ogg')

    transcript = await gpt_voice_to_text(f'{voice_path}.mp3')

    await message.reply(text=transcript.text)

    os.remove(f'{voice_path}.mp3')


@chat.message()
async def chat_message(message: Message):
    chat_tg_id = int(message.chat.id)
    user_tg_id = int(message.from_user.id)
    await add_user_to_chat(chat_tg_id=chat_tg_id, user_tg_id=user_tg_id)

    if '@all' in message.text:
        await mention_all_users(message=message)
