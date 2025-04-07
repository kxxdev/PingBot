import httpx
from openai import AsyncOpenAI

from config import OPENAI_TOKEN, PROXY

client = AsyncOpenAI(api_key=OPENAI_TOKEN,
                     http_client=httpx.AsyncClient(proxy=PROXY))


async def gpt_voice_to_text(file_path):
    file = open(file_path, 'rb')
    return await client.audio.transcriptions.create(
        model='gpt-4o-transcribe',
        file=file
    )
