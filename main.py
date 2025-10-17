# main.py - SantaGumi Discord Bot (24h Render-ready)
import os, sys, asyncio, logging, importlib, pkgutil
from typing import List
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

# ───────────────────────────────
# 1) Flask keep-alive (Render ping)
# ───────────────────────────────
app = Flask(__name__)

@app.get("/")
def home():
    return "SantaGumi Bot is alive! 🎅", 200

def run_keepalive():
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_keepalive, daemon=True)
    t.start()

# ───────────────────────────────
# 2) Discord bot setup
# ───────────────────────────────
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s | %(message)s")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# ───────────────────────────────
# 3) Auto-load cogs from /cogs folder
# ───────────────────────────────
def list_cogs(package_name: str = "cogs") -> List[str]:
    modules = []
    try:
        pkg = importlib.import_module(package_name)
    except ModuleNotFoundError:
        logging.warning("⚠️ No 'cogs' folder found. Add your feature files there.")
        return modules

    for mod in pkgutil.iter_modules(pkg.__path__):
        if not mod.ispkg:
            modules.append(f"{package_name}.{mod.name}")
    return modules

async def load_all_cogs():
    cogs = list_cogs()
    if not cogs:
        logging.warning("⚠️ No cogs to load.")
        return
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logging.info(f"✅ Loaded {cog}")
        except Exception as e:
            logging.error(f"❌ Failed to load {cog}: {e}")

# ───────────────────────────────
# 4) Events and commands
# ───────────────────────────────
@bot.event
async def on_ready():
    logging.info(f"🎅 Logged in as {bot.user} (id: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="Serving the North Pole 🎁"))
    try:
        synced = await bot.tree.sync()
        logging.info(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        logging.error(f"❌ Slash sync failed: {e}")

@bot.tree.command(name="ping", description="Check SantaGumi bot status")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🎄 pong! SantaGumi is alive!", ephemeral=True)

# ───────────────────────────────
# 5) Start the bot
# ───────────────────────────────
async def main():
    token = os.getenv("TOKEN")
    if not token:
        logging.error("❌ TOKEN not found in environment variables.")
        sys.exit(1)

    keep_alive()
    await load_all_cogs()

    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
