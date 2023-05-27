# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='help')
async def help_command(ctx):
    help_text = 'Welcome to the bot! I can help you'

    await ctx.send(response)

bot.run(TOKEN)