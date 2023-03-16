import os
import random
import webcolors
import sparkutils #custom utility library
import discord #discord api
import requests #enable web requests
import importlib #dynamic function importing
from dotenv import load_dotenv #for file-based OAuth
from discord.ext import commands #i command ye
from discord import Embed #pretty embeds


#get user OAuth Token
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

#state our intent with the bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guild_messages = True
intents.dm_messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

#create bot object
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
bot = commands.Bot(
    command_prefix = commands.when_mentioned_or('!'),
    description = sparkutils.read_file('README.md'),
    help_command = help_command,
    intents = intents
)

#----------------------------------------------
# EVENTS
#----------------------------------------------
@bot.event #log successful startup to the console
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
@bot.event #in the event a user sends a bad command
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None and not message.content.startswith('!'):
        await message.channel.send('Hello! This is a DM message. If you want to use commands, please use the prefix `!`.')

    await bot.process_commands(message)
#----------------------------------------------
# COMMANDS
#----------------------------------------------
@bot.command(name='xarc', help='Executes a fucntion from arcs.py.')
async def xarc(ctx, function_name: str, *args: str):
    try:
        functions_module = importlib.import_module("arcs")
        # Reload the module to get the latest version
        importlib.reload(functions_module)
        function = getattr(functions_module, function_name, None)

        #check if the function exists and can be run
        if function is not None and callable(function):
            result = function(*args)
            #create the embed object
            embed = discord.Embed(title=f"Function `{function_name}` executed", color=discord.Color.green())
            embed.add_field(name="Result", value=result, inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Function `{function_name}` not found in arcs.py", color=discord.Color.red())
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title=f"Error executing function `{function_name}`", color=discord.Color.orange())
        embed.add_field(name="Error", value=str(e), inline=False)
        await ctx.send(embed=embed)
        
#----------------------------------------------
# START BOT
#----------------------------------------------
bot.run(TOKEN)