
import os, sys, asyncio, discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread

# -------------------------
# Keep-alive Flask server (Render용)
# -------------------------
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return "Bot is alive!", 200

def run():
    app.run(host="0.0.0.0", port=8080)

# Flask는 백그라운드 스레드로 실행
Thread(target=run, daemon=True).start()

# -------------------------
# Discord bot
# -------------------------

# Render에서 audioop 에러 방지
sys.modules["audioop"] = None

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 봇이 켜졌어요! Logged in as {bot.user} (id: {bot.user.id})")

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
