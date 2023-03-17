import os
import io
import asyncio  # might conflict with io
import aiohttp
import random
import sparkutils  # custom utility library
import discord  # discord api
import requests  # enable web requests
import importlib  # dynamic function importing
from dotenv import load_dotenv  # for file-based OAuth
from discord.ext import commands  # i command ye
from discord import Embed  # pretty embeds
import json
import base64
from PIL import Image, PngImagePlugin


'''
MODULAR FUNCTION IMPORTS
TODO:
Create a directory structure for including multiple arc files
Add some kind of cloud sync or user code submission method
'''
functions_module = importlib.import_module("arcs")

baseprompt = "optimistic solarpunk future, humans and ai working together, harmony, sustainable architecture, vibrant flora"

# get user OAuth Token
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# state our intent with the bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guild_messages = True
intents.dm_messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

# create bot object
help_command = commands.DefaultHelpCommand(
    no_category='Commands'
)
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description=sparkutils.read_file('README.md'),
    help_command=help_command,
    intents=intents
)

'''
# EVENTS
'''


@bot.event  # log successful startup to the console
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event  # in the event a user sends a bad command
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None and not message.content.startswith('!'):
        await message.channel.send('Hello! This is a DM message. If you want to use commands, please use the prefix `!`.')

    await bot.process_commands(message)
'''
# COMMANDS
'''


@bot.command(name='xarc', help='Executes a fucntion from arcs.py.')
async def xarc(ctx, function_name: str, *args: str):
    print(sparkutils.ctx_info(ctx))
    try:
        # Reload the module to get the latest version
        importlib.reload(functions_module)
        function = getattr(functions_module, function_name, None)

        # check if the function exists and can be run
        if function is not None and callable(function):
            result = function(*args)
            # create the embed object
            embed = discord.Embed(
                title=f"Function `{function_name}` executed", color=discord.Color.green())
            embed.add_field(name="Result", value=result, inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"Function `{function_name}` not found in arcs.py", color=discord.Color.red())
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title=f"Error executing function `{function_name}`", color=discord.Color.orange())
        embed.add_field(name="Error", value=str(e), inline=False)
        await ctx.send(embed=embed)


@bot.command(name='invert', help='Inverts the colors of the image attached to the message.')
async def invert(ctx):
    if not ctx.message.attachments:
        await ctx.send("Please attach an image to your message.")
        return

    attachment = ctx.message.attachments[0]
    image_bytes = await attachment.read()

    image = Image.open(io.BytesIO(image_bytes))
    image_rgb = image.convert("RGB")  # Convert the image to RGB mode
    inverted_image = ImageOps.invert(image_rgb)

    with io.BytesIO() as output:
        inverted_image.save(output, format="PNG")
        output.seek(0)
        await ctx.send(file=discord.File(output, "inverted_image.png"))

'''
TEXT2IMAGE USING AUTOMATIC1111 API
'''


@bot.command(
    name='text2img',
    aliases=['t2i', 'dream'],
    brief='Generate images using StableDiffusion.',
    description='LongDesc WIP.',
    help='Help WIP',
    usage='!text2img "<prompt>" <quality> <guidance> <batchsize>',
    rest_is_raw=False,
    ignore_extra=True,
    cooldown_after_parsing=True,
    hidden=False,
)
async def t2i(
    ctx,
    prompt: str = commands.parameter(
        default=baseprompt, description="Image prompt"),
    quality: int = commands.parameter(
        default=2, description="Quality setting for the image"),
    guidance: int = commands.parameter(
        default=7, description="Guidance for image generation"),
    batchsize: int = commands.parameter(
        default=1, description="Number of images to generate in a batch")
):
    url = "http://127.0.0.1:7860"
    try:
        health_check = requests.get(url)
        if health_check.status_code != 200:
            await ctx.send("The web service is not up or responsive. Please check the service and try again.")
            return
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error connecting to the web service: {e}")
        return

    payload = {
        "prompt": prompt,
        "steps": quality*10,
        "batch_size": batchsize,
        "cfg_scale": guidance
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        imgreponse = requests.post(
            url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", imgreponse.json().get("info"))

        with io.BytesIO() as output:
            image.save(output, format='PNG', pnginfo=pnginfo)
            output.seek(0)
            await ctx.send(file=discord.File(output, "output.png"))
'''
Command Example
'''


@bot.command(
    name='example',
    aliases=['ex', 'sample'],
    brief='An example command.',
    description='This is an example command that demonstrates various parameters of the @bot.command() decorator.',
    help='Use this command to see how different parameters affect the command help output.',
    usage='!example',
    rest_is_raw=False,
    ignore_extra=True,
    cooldown_after_parsing=True,
    hidden=False,
)
async def example(
        ctx,
        strparam: str = commands.parameter(
            default="string parameter", description="Example string parameter"),
        intparam: int = commands.parameter(
            default=42, description="Example int parameter")):
    await ctx.send(f'This is an example command. The arguments passed were {strparam}, and {intparam}')
'''
# START BOT
'''
bot.run(TOKEN)
