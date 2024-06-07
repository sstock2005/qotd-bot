
# Quote of the Day Discord Bot

A simple discord bot that sends a random quote every day at 1:00PM CDT (6:00PM UCT). Don't ask about the hello command, I forgot to delete it and may get around to it sometime.  

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
![image](https://github.com/sstock2005/qotd-bot/assets/144393153/ab289197-dabf-4190-94a0-2c490f489d96)  
![image](https://github.com/sstock2005/qotd-bot/assets/144393153/26de2d16-13b4-4fe2-b601-2162ad10d6c2)

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
        - You may need to create a new directory for this!

## Installation
```
git clone [repo link]
pip install -r requirements.txt
py bot.py
``` 
