from discord.ext import commands

client = commands.Bot(
    command_prefix = '/',
    help_command = None
)

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

client.run('')