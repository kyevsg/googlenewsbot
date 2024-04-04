import os

import discord
from discord.ext import app_commands, tasks
from dotenv import load_dotenv

from scraper import scraper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = app_commands.Bot(command_prefix = '!')
bot.remove_command("help")

MY_GUILD = discord.Object(id=0)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

client.run(TOKEN)

@client.tree.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(bot.latency * 1000)} ms')


@client.tree.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Color.blue(),
        title="Help",
        description="Available functions"
    )

    embed.add_field(name="/ping", value="This command returns the bot's latency", inline=False)
    embed.add_field(name="/news-setup [channel] [keywords included] [keywords excluded]",
                    value="The bot answers with number of articles of the given country in the given language ",
                    inline=False)

    await ctx.send(embed=embed)