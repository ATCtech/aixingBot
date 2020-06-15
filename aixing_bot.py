# aixing_bot.py
# A discord bot created by Mikey San
# This is mostly a tutorial project for use on my discord server.

import os
import random

import discord
from discord.ext import commands
from discord import activity, message

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

import logging


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    status = discord.Status.online
    channel = discord.utils.get(guild.channels, name="random-chat")
    wave = ":wave:"
    # await client.change_presence(activity=activity, status=status)
    # await client.send(f'Aweomeness has arrived in {channel}')
    await channel.send(f'A Champion has arrived {wave}')


# Allow a user with admin role the ability to create a channel using our bot
@client.command(name='create-channel', help='Create a channel using create-channel followed by channel name')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='bot-chat'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

# Add an error check to inform a user if they do not have permisison to run this command.
# Normally, the error message is not shown to the user so there is no way for them to know why it didn't work
# This event ensures that they know why.

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


# Let's open our file and read something from it.
@client.command(name='treky', help='Responds with random quote from Star Trek')
async def treky(ctx):
    with open("stquotes.txt", "r") as f:
        lines = f.readlines()
        response = random.choice(lines)
    await ctx.send(response)


client.run(TOKEN)