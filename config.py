import os
from dotenv import load_dotenv
load_dotenv()


def send_value_error(var):
    raise ValueError(f'Переменная {var} не найдена в .env')


TOKEN = os.getenv('TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
PROXY = os.getenv('PROXY')

if TOKEN is None:
    send_value_error('TOKEN')
if OPENAI_TOKEN is None:
    send_value_error('OPENAI_TOKEN')
if PROXY is None:
    send_value_error('PROXY')
