from config import BASE_FOLDER
import random
import json
import os

def initialize_guild(guild):
    os.makedirs(os.path.join(BASE_FOLDER, str(guild.id)), exist_ok=True)
    
def write_guild_settings(guild, quote_of_the_day_channel, commands_channel):
    settings = {
        "quote_of_the_day_channel": quote_of_the_day_channel.id,
        "commands_channel": commands_channel.id
    }
    
    with open(os.path.join(BASE_FOLDER, str(guild.id), "settings.json"), "w") as f:
        json.dump(settings, f)

def read_guild_settings(guild):
    if os.path.exists(os.path.join(BASE_FOLDER, str(guild.id), "settings.json")) == False:
        return None
    
    with open(os.path.join(BASE_FOLDER, str(guild.id), "settings.json"), "r") as f:
        return json.load(f)

def write_quote(guild, quote, author):
    file_path = os.path.join(BASE_FOLDER, str(guild.id), "quotes.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                quotes = json.load(f)
            except json.JSONDecodeError:
                quotes = []
    else:
        quotes = []

    quotes.append({"quote": quote, "author": author, "used": False})

    with open(file_path, "w") as f:
        json.dump(quotes, f)

def read_quote(guild):
    file_path = os.path.join(BASE_FOLDER, str(guild.id), "quotes.json")

    if not os.path.exists(file_path):
        return None, None

    with open(file_path, "r") as f:
        try:
            quotes = json.load(f)
        except json.JSONDecodeError:
            return None, None

    unused_quotes = [quote for quote in quotes if not quote["used"]]
    if not unused_quotes:
        for quote in quotes:
            quote["used"] = False
        unused_quotes = quotes

    selected_quote = random.choice(unused_quotes)
    selected_quote["used"] = True

    with open(file_path, "w") as f:
        json.dump(quotes, f)

    return selected_quote["quote"], selected_quote["author"]