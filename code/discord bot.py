#Packages
import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

#Load secrets
load_dotenv()

#Discord bot permissions
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

#Create discord bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

#Input output discord channels
SOURCE_CHANNEL_ID = int(os.getenv('INPUT'))
TARGET_CHANNEL_ID = int(os.getenv('TEMP_OUTPUT'))

# Keywords to look for in the title
MAIN_UPDATE_KEYWORDS = ["awakening of the primals",  "grave of eden",
    "eternity summit",
    "ancient dragon",
    "xil",
    "t15 weapons",
    "t15 armor",
    "world boss"]

#Title webscraping function
async def fetch_page_title(url):
    """Fetch the title of a webpage given its URL."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                title = soup.title.string if soup.title else ""
                return title.strip()
        except Exception as e:
            print(f"Error fetching page: {url}\n{e}")
            return ""

#Logged in notification
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

#Reads messages from input
@bot.event
async def on_message(message):
    if message.author != bot.user:  #Make sure bot doesnt respond to itself (not needed but just in case)
        if message.channel.id == SOURCE_CHANNEL_ID:
            for word in message.content.split():
                if word.startswith("http://") or word.startswith("https://"):
                    page_title = await fetch_page_title(word)
                    title_lower = page_title.lower()

                    if any(keyword in title_lower for keyword in MAIN_UPDATE_KEYWORDS):
                        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
                        if target_channel:
                            await target_channel.send(f"@everyone 🚨 ENDGAMESTUFF!: **{page_title}**\n{word}")
                            print(f"🔔 Matched keyword in title: {page_title}")
                    else:
                        print(f"⏸ No keywords found in title: {page_title}")

        await bot.process_commands(message)


print("Token from .env:", os.getenv('DISCORD_KEY'))
# Run the bot with your token
bot.run(os.getenv('DISCORD_KEY'))