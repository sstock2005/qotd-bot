
# Quote of the Day Discord Bot

A simple discord bot that sends a random quote every day at 1:00PM CDT (6:00PM UCT).

- Multiple Guild Support
- Simple but powerful user commands
- Handles correct authority checks against users
- Small and powerful database logic

## Application commands
- `/add_quote <quote> <author>`
    - **Requires Admin or Poet Role**
    - Adds given quote with the author into the guild specific database
- `/quote_now`
    - **Requires Admin or Poet Role**
    - Bypasses the wait task and sends a quote to the quote channel immediately
- `/setup <quote of the day channel> <bot commands channel>`
    - **Requires Admin**
    - Required before all other commands will work. This saves the given channels into the guild specific settings databse.
- `/clear_quotes`
    - **Requires Admin**
    - Clears guild specific quote database.

## Showcase
[image here] 

## Storage Logic
- Creates new folder for each guild joined.
    - The folder name is the guild `id`.
- Stores guild specific data in `settings.json` and `quotes.json`
- Deletes guild folder when the bot is kicked or leaves the server.

## Requirements
- Tested on Python 3.12.3, and Windows 11
- Edit `config.py`
    - Add your discord bot token
    - Add your base directory (`./guilds`)

## Installation
```
git clone [repo link]
pip install -r requirements.txt
py bot.py
``` 