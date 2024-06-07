from helper import initialize_guild, read_guild_settings, write_guild_settings, write_quote, read_quote
from config import BASE_FOLDER, DISCORD_TOKEN, primary_colors
from discord import app_commands
from discord.ext import tasks
import asyncio
import datetime
import discord
import logging
import shutil
import random
import os

logging.basicConfig(filename='discord.log', level=logging.INFO)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        for name in [name for name in os.listdir(BASE_FOLDER) if os.path.isdir(os.path.join(BASE_FOLDER, name))]:
            logging.info("Syncing to Guild: " + name)
            try:
                self.tree.copy_global_to(guild=discord.Object(id=name))
                await self.tree.sync(guild=discord.Object(id=name))
            except discord.errors.Forbidden:
                logging.error("Failed to sync to Guild: " + name)
                continue

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user} (ID: {client.user.id})')
    quote_of_the_day.start()

@client.event
async def on_guild_join(guild):
    logging.info(f'Joined guild {guild.name} (ID: {guild.id})')
    initialize_guild(guild)
    await guild.create_role(name='Poet')
    client.tree.copy_global_to(guild=guild)
    await client.tree.sync(guild=guild)

@client.event
async def on_guild_remove(guild):
    logging.info(f'Left guild {guild.name} (ID: {guild.id})')
    try:
        shutil.rmtree(os.path.join(BASE_FOLDER, str(guild.id)))
    except Exception as e:
        logging.error(f'Failed to remove guild {guild.name} (ID: {guild.id}): {e}')
        
@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')
    return

@client.tree.command()
async def setup(interaction: discord.Interaction, quote_of_the_day_channel: discord.TextChannel, commands_channel: discord.TextChannel):
    """Required Setup Command"""
    if interaction.user.guild_permissions.administrator:
        if read_guild_settings(interaction.guild) == None:
            write_guild_settings(interaction.guild, quote_of_the_day_channel, commands_channel)
            await interaction.response.send_message("Setup complete! Try running /add_quote!", ephemeral=True)
            return
        else:
            await interaction.response.send_message("You have already run /setup!", ephemeral=True)
            return
    else:
        await interaction.response.send_message("You must be an administrator to run this command.", ephemeral=True)
        return
        
@client.tree.command()
async def add_quote(interaction: discord.Interaction, quote: str, author: str):
    """Add a quote!"""
    if read_guild_settings(interaction.guild) == None:
        await interaction.response.send_message("You must run /setup first!", ephemeral=True)
        return
    
    guild_settings = read_guild_settings(interaction.guild)
    
    if guild_settings is not None and interaction.channel_id == guild_settings["commands_channel"]:
        if any(role.name == 'Poet' for role in interaction.user.roles) or interaction.user.guild_permissions.administrator:
            write_quote(interaction.guild, quote, author)
            await interaction.response.send_message("Quote added!", ephemeral=True)
            return
        else:
            await interaction.response.send_message('You must be an administrator or have the role Poet to use this command.', emphemeral=True)
            return
    else:
        await interaction.response.send_message("You must run this command in the commands channel.", emphemeral=True)
        return

@client.tree.command()
async def quote_now(interaction: discord.Interaction):
    """Get a quote now!"""
    if read_guild_settings(interaction.guild) == None:
        await interaction.response.send_message("You must run /setup first!", ephemeral=True)
        return
    
    guild_settings = read_guild_settings(interaction.guild)
    
    if guild_settings is not None and interaction.channel_id == guild_settings["commands_channel"]:
        if any(role.name == 'Poet' for role in interaction.user.roles) or interaction.user.guild_permissions.administrator:
            quote, author = read_quote(interaction.guild)
            if quote is None or author is None:
                await interaction.response.send_message("No quotes found.", emphemeral=True)
                return
            
            channel = client.get_channel(read_guild_settings(interaction.guild)["quote_of_the_day_channel"])
            embed = discord.Embed(title=f"{quote}", description=f"-{author}", color=random.choice(primary_colors), timestamp=datetime.datetime.now())
            embed.set_footer(text="Discord Bot By Sam Stockstrom")
            await channel.send(embed=embed)
            
            await interaction.response.send_message("Pushed quote to the correct channel!", ephemeral=True)
            return
        else:
            await interaction.response.send_message('You must be an administrator or have the role Poet to use this command.', emphemeral=True)
            return
    else:
        await interaction.response.send_message("You must run this command in the commands channel.", emphemeral=True)
        return
    
@client.tree.command()
async def clear_quotes(interaction: discord.Interaction):
    """Clear saved quotes!"""
    if read_guild_settings(interaction.guild) == None:
        await interaction.response.send_message("You must run /setup first!", ephemeral=True)
        return
    
    guild_settings = read_guild_settings(interaction.guild)
    
    if guild_settings is not None and interaction.channel_id == guild_settings["commands_channel"]:
        if interaction.user.guild_permissions.administrator:
            file_path = os.path.join(BASE_FOLDER, str(interaction.guild.id), "quotes.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                await interaction.response.send_message("Quotes cleared!", ephemeral=True)
                return
            else:
                await interaction.response.send_message("No quotes found.")
                return
        else:
            await interaction.response.send_message('You must be an administrator to use this command.', emphemeral=True)
            return
    else:
        await interaction.response.send_message("You must run this command in the commands channel.", emphemeral=True)
        return

@tasks.loop(hours=24)
async def quote_of_the_day():
    if len(client.guilds) == 0:
        logging.info("No guilds found.")
        await asyncio.sleep(60 * 60)
        
    now = datetime.datetime.now(datetime.UTC)
    logging.info("Current time: " + str(now))
    
    if now.hour < 18:
        wait_for = datetime.timedelta(hours=18) - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        logging.info("Waiting for: " + str(wait_for.total_seconds()))  
        await asyncio.sleep(wait_for.total_seconds())
        
    for name in [name for name in os.listdir(BASE_FOLDER) if os.path.isdir(os.path.join(BASE_FOLDER, name))]:
        if read_guild_settings(discord.Object(id=name)) is None:
            await asyncio.sleep(60 * 60)
            
        channel = client.get_channel(read_guild_settings(discord.Object(id=name))["quote_of_the_day_channel"])
        
        quote, author = read_quote(discord.Object(id=name))
        if quote is None or author is None:
            logging.error("No quotes found for guild in task: " + name)
            await asyncio.sleep(60 * 60)
        
        embed = discord.Embed(title=f"{quote}", description=f"-{author}", color=random.choice(primary_colors), timestamp=datetime.datetime.now())
        embed.set_footer(text="Discord Bot By Sam Stockstrom")
        await channel.send(embed=embed)
        
client.run(DISCORD_TOKEN)