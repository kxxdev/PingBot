import os
from dotenv import load_dotenv
load_dotenv()


def send_value_error(var):
    raise ValueError(f'Переменная {var} не найдена в .env')


TOKEN = os.getenv('TOKEN')

if TOKEN is None:
    send_value_error('TOKEN')
