import os

import discord
from discord import app_commands
from discord.ext import tasks

from dotenv import load_dotenv

from scraper import scraper

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


MY_GUILD = discord.Object(id=)  # add your server id here


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


@client.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'pong! {round(client.latency * 1000)} ms')


@client.tree.command()
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        colour=discord.Color.blue(),
        title="Help",
        description="Available functions"
    )

    embed.add_field(name="/ping", value="This command returns the bot's latency", inline=False)
    embed.add_field(name="/news_setup [channel] [keyword]",
                    value="The bot sends article links to your channel of choice every hour",
                    inline=False)
    embed.add_field(name="/news_remove", value="This command removes the setup news at its list index", inline=False)
    embed.add_field(name="/news_display", value="This command returns the news list", inline=False)

    await interaction.response.send_message(embed=embed)

# News Bot
news_array = []  # array to contain news_setup command info


@client.tree.command()
async def news_setup(interaction: discord.Interaction, channel: discord.TextChannel, keyword: str):
    news_array.append([channel, keyword])
    await interaction.response.send_message(f'News feed set up in {channel}!')


@tasks.loop(hours=1)
async def fetch_article():
    await discord.client.wait_until_ready()
    for item in news_array:
        channel = item[0]
        entries = scraper(item[1])
        for entry in entries:
            await channel.send(entry.link)


@client.tree.command()
async def news_remove(interaction: discord.Interaction, index: int):
    del news_array[index]
    await interaction.response.send_message(f'Index {index} removed!')


@client.tree.command()
async def news_display(interaction: discord.Interaction):
    await interaction.response.send_message(f'{news_array}')


client.run(TOKEN)
