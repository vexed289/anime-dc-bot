import discord
from discord.ext import commands

def createBot() -> commands.Bot:

    variables = {}
    intents = discord.Intents.default()
    intents.message_content = True

    return commands.Bot(command_prefix='!', 
                        intents=intents)