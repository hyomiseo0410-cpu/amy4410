from flask import Flask
from threading import Thread
import os, asyncio, discord, sys
from discord.ext import commands

# keep alive web server for render
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"
def run():
    app.run(host="0.0.0.0", port=8080)
Thread(target=run).start()

# prevent audioop error
sys.modules["audioop"] = None

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id: {bot.user.id})")

from discord import app_commands
@bot.tree.command(name="ping", description="Check bot status")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!", ephemeral=True)

async def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ TOKEN env var missing")
        return
    try:
        await bot.start(token)
    finally:
        await bot.close()

asyncio.run(main())
