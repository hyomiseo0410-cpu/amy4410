
import os, sys, asyncio, discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

# Flask keep-alive server
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return "Bot is alive!", 200

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run, daemon=True).start()

# prevent audioop import error
sys.modules["audioop"] = None

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id: {bot.user.id})")

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

if __name__ == "__main__":
    asyncio.run(main())
