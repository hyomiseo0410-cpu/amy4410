import os, asyncio, discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id: {bot.user.id})")

# 예시 slash 명령어
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

if __name__ == "__main__":
    asyncio.run(main())
