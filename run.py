# run.py
import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv
from db import record_bet
from markov import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents = intents)

# TODO: Argument type validation
# TODO: Hide/delete command messages
@bot.command(name='bet')
async def bet(ctx, gold):
    # TODO: Find active session from db, if no active sessions reject.
    await record_bet(ctx.author, gold)
    response = f'Nice! You have bet {gold} gold, best of luck!'

    await ctx.send(response)

# TODO: Just use admin permission for the method after testing's done
@bot.command(name='start')
@commands.has_permissions(administrator=True)
async def start_bet(ctx, start_rolls, desired_p=50):
    start = int(start_rolls)
    if start > 10000:
        await ctx.author.send('Sorry, max amount is 10000')

    response = ''

    # TODO: Create a new session
    ideal_roll_num = await get_ideal_rolls(start, float(desired_p)/100)
    response = f'You\'ve started a bet! \nHouse roll should be {ideal_roll_num}.'
    
    await ctx.author.send(response)
    await ctx.send(f'A bet has started for {start}! Place your bet now :)')


@bot.command(name='end')
@commands.has_permissions(administrator=True)
async def end_bet(ctx, houseWon):
    # TODO: End current bet session, update in db

    if houseWon == 'yes':
        await ctx.send('Bet has ended, house won. Better luck next time!')
    else:
        await ctx.send('Bet has ended, you won! Hooray!')

bot.run(TOKEN)
