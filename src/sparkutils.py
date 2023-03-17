import discord  # discord api
import datetime

def read_file(filename):
    """Reads a file and returns the contents as a string

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(filename, 'r') as f:
        return f.read()


def ctx_info(ctx):
    """Unpacks a Discord context object and returns the data

    Args:
        ctx (_type_): _description_

    Returns:
        _type_: _description_
    """
    attrs = ['author', 'channel', 'guild', 'bot']  # 'message',
    output = ''
    for attr in attrs:
        value = getattr(ctx, attr, None)
        if value is not None:
            output += f'{attr}: {value}\n'
    return output


def format_embed(title, description, color, fields, footer):
    """Accepts various data as input and outputs a formatted discord message embed object

    Args:
        title (_type_): _description_
        description (_type_): _description_
        color (_type_): _description_
        fields (_type_): _description_
        footer (_type_): _description_

    Returns:
        _type_: _description_
    """
    embed = discord.Embed(title=title, description=description, color=color)
    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=field[2])
    embed.set_footer(text=footer)
    return embed

def get_current_time():
    """returns the current date and time as a human reable string 12 hour time format and AM/PM


    Returns:
        datetime (str): the formatted date and time
    """    
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y %I:%M %p")
