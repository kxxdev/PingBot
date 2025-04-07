# Telegram @all Bot

A simple Telegram bot that pings up to 10 users in a chat when someone sends `@all`.  
Useful for small group chats to notify everyone.

---

## 🚀 Features

- Detects `@all` in group messages
- Replies by mentioning up to 10 users
- Easily customizable
- Lightweight and fast

---

## Create .env file

Create a .env file in the root directory with your bot token:

```
TOKEN='your-telegram-token-here'
```

## Install dependencies

We recommend using a virtual environment:

```
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r reqs.txt

```

## Run the bot

```
python run.py
```

# Docker (Optional)

To run with Docker:

```
docker build -t telegram-all-bot .
docker run -d --env-file .env telegram-all-bot
```

## Note

- Make sure the bot is added to a group.
- It needs permission to read messages and mention users.
- You may need to promote the bot as an admin depending on group settings.
