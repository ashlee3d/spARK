import discord #discord api
'''
Reads a file and returns the contents as a string
'''
def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()
'''
Unpacks a Discord context object and returns the data
'''
def ctx_info(ctx):
    attrs = ['author', 'channel', 'guild', 'bot']#'message',
    output = ''
    for attr in attrs:
        value = getattr(ctx, attr, None)
        if value is not None:
            output += f'{attr}: {value}\n'
    return output
'''
Accepts various data as input and outputs a formatted discord message embed object
'''
def format_embed(title, description, color, fields, footer):
    embed = discord.Embed(title=title, description=description, color=color)
    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=field[2])
    embed.set_footer(text=footer)
    return embed

