import os
from keep_alive import keep_alive
from discord.ext import commands
import discord

intents = discord.Intents(
    guilds=True, members=True, messages=True, reactions=True,
    bans=False, emojis=False, integrations=False, webhooks=False, invites=False, voice_states=False, presences=False,
    typing=False
)

bot = commands.Bot(
	command_prefix="?",  # Change to desired prefix
	case_insensitive=True,  # Commands aren't case-sensitive
  intents=intents
)

bot.author_id = 623277032930803742  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
	'cogs.devtools','cogs.usertools', 'cogs.admintools'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot