# run.py
import os
import discord

from threading import *
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from db import record_bet, create_new_session, end_session_and_get_results
from markov import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.messages = True
intents.members = True

class botClient(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = True
        self.added = True
    
    async def on_ready(self):
        # await tree.sync()
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=GUILD_ID))
            self.synced = True
        if not self.added:
            self.added = True
        print("Hello world")

client = botClient()
tree = app_commands.CommandTree(client)

@tree.command(description='Place a bet', guild = discord.Object(id=GUILD_ID))
async def bet(interaction: discord.Interaction, gold: int):
    if gold <= 0:
        await interaction.response.send_message('Sneaky you, but that\'s not a valid number :P', ephemeral = True)
        return

    try:
        record_bet(interaction.user, gold)
    except Exception as e:
        await interaction.response.send_message(str(e), ephemeral = True)
        return

    response = f'{interaction.user.display_name} have bet {gold} gold, best of luck!'
    await interaction.response.send_message(response)


@tree.command(description='Start a bet', guild = discord.Object(id=GUILD_ID))
@commands.has_permissions(administrator=True)
async def start(interaction: discord.Interaction, pool_amount: int):
    if pool_amount > 5000:
        await interaction.response.send_message('Sorry, max betting pool is 5000', ephemeral = True)
        return
    elif pool_amount <= 0:
        await interaction.response.send_message('Invalid betting pool number. Try again please!', ephemeral = True)
        return

    try:
        create_new_session(pool_amount)
    except Exception:
        await interaction.response.send_message('A bet is already on going, cannot start a new one.', ephemeral = True)
        return

    await interaction.response.send_message('Bet successfully started ;)', ephemeral = True)
    await interaction.channel.send(f'A side bet has started for {pool_amount} gold! Place your bet now :)')

@tree.command(description='Calculate house roll and win rate', guild = discord.Object(id=GUILD_ID))
@commands.has_permissions(administrator=True)
async def calc(interaction: discord.Interaction, starting_roll: int, desired_p: int):
    await interaction.response.send_message('Beep boop, computing the odds...', ephemeral = True)

    (ideal_roll_num, p) = get_ideal_rolls(starting_roll, float(desired_p)/100)
    await interaction.user.send(f'Starting roll is {starting_roll}! \nHouse roll should be {ideal_roll_num}, \nPercentage is {p * 100}.')

@tree.command(description='End the bet', guild = discord.Object(id=GUILD_ID))
@commands.has_permissions(administrator=True)
async def end(interaction: discord.Interaction, house_won_yes_or_no: str):
    if house_won_yes_or_no != 'yes' and house_won_yes_or_no != 'no':
        await interaction.response.send_message('Not valid input, use \'yes\' or \'no\'!', ephemeral = True)
        return

    house_won = True if house_won_yes_or_no.lower() == 'yes' else False
    results = end_session_and_get_results()

    members_dict = {}
    async for member in interaction.guild.fetch_members(limit=None):
        members_dict.update({str(member): member.display_name})

    message_head = f"Betting has ended, the {'house' if house_won else 'players'} won! Here are the results: \n"
    responses = [message_head]
    for (userid, amount) in results:
        display_name = members_dict.get(userid)
        if house_won:
            responses.append(f'☆ {display_name} lost {amount} gold\n')
        else:
            responses.append(f'★ {display_name} won {amount} gold\n')
    
    await interaction.response.send_message("".join(responses))

client.run(TOKEN)
