import os
import random
import sparkutils #custom utility library
import discord #discord api
import requests #enable web requests
import importlib #dynamic function importing
from dotenv import load_dotenv #for file-based OAuth
from discord.ext import commands #i command ye
from discord import Embed #pretty embeds
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModelForCausalLM
from read import read_config
from argparse import ArgumentParser
import torch
import time
def generate(tokenizer, prompt, model, config):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)

    outputs = model.generate(input_ids=input_ids, max_new_tokens=config["max_new_tokens"], temperature=config["temperature"])

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    return decoded[len(prompt):]

    
def setup_model(config):
    model = AutoModelForCausalLM.from_pretrained(config["model_name"], device_map="auto", torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained(config["tokenizer_name"])
    added_tokens = tokenizer.add_special_tokens({"bos_token": "<s>", "eos_token": "</s>", "pad_token": "<pad>"})

    if added_tokens > 0:
        model.resize_token_embeddings(len(tokenizer))

    if config["lora"]:
        model = PeftModelForCausalLM.from_pretrained(model, config["lora_path"], device_map="auto", torch_dtype=torch.float16)
        model.to(dtype=torch.float16)

    print(f"Mem needed: {model.get_memory_footprint() / 1024 / 1024 / 1024:.2f} GB")
        
    return model, tokenizer
model, tokenizer = setup_model(config)
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
#log successful startup to the console
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#test command

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None and not message.content.startswith('!'):
        await message.channel.send('Hello! This is a DM message. If you want to use commands, please use the prefix `!`.')

    await bot.process_commands(message)

#----------------------------------------------
# COMMANDS
#----------------------------------------------
@bot.command(name='hello', help='Says hello to the user.')
async def hello(ctx, prompt:str):
    await ctx.send(f'Hello {ctx.author.mention}!')


@bot.command(name='gen', help='generates text')
async def gen(ctx, *, prompt):
    generation = generate(tokenizer, prompt, model, config)
    return await ctx.send(generation)
@bot.command(name='randimg', help='Sends a random image from Wikimedia Commons.')
async def randimg(ctx):
    url = "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=random&rnnamespace=6&rnlimit=1"
    response = requests.get(url)
    data = response.json()

    image_title = data['query']['random'][0]['title']
    image_url = f"https://commons.wikimedia.org/wiki/{image_title.replace(' ', '_')}"

    image_info_url = f"https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles={image_title}"
    response = requests.get(image_info_url)
    data = response.json()

    image_direct_url = list(data['query']['pages'].values())[0]['imageinfo'][0]['url']

    embed = discord.Embed(title=image_title, url=image_url, color=random.randint(0, 0xFFFFFF))
    embed.set_image(url=image_direct_url)

    await ctx.send(embed=embed)

#respond to messages that dont fit a commmand template

@bot.command(name='xarc', help='Executes a fucntion from arcs.py.')
async def xarc(ctx, function_name: str, *args: str):
    try:
        functions_module = importlib.import_module("arcs")
        # Reload the module to get the latest version
        importlib.reload(functions_module)
        function = getattr(functions_module, function_name, None)

        if function is not None and callable(function):
            result = function(*args)

            embed = discord.Embed(title=f"Function `{function_name}` executed", color=0x00FF00)
            embed.add_field(name="Result", value=result, inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Function `{function_name}` not found in arcs.py", color=0xFF0000)
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title=f"Error executing function `{function_name}`", color=0xFFA500)
        embed.add_field(name="Error", value=str(e), inline=False)
        await ctx.send(embed=embed)
#----------------------------------------------
# START BOT
#----------------------------------------------
bot.run(TOKEN)
