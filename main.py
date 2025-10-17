# main.py
import os
import asyncio
import logging
from threading import Thread

from flask import Flask
import discord
from discord.ext import commands

# ----------------------------
# 0. 로그 설정 (Render 로그에서 보기 좋게)
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ----------------------------
# 1) Render 헬스 체크용 웹 서버
# ----------------------------
app = Flask(__name__)

@app.get("/")
def index():
    return "WOSBot is alive! ✅", 200

def run_web():
    # Render가 할당한 PORT를 사용해야 포트 스캐너에 잡힙니다.
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web, daemon=True)
    t.start()

# ----------------------------
# 2) Discord Bot
# ----------------------------
intents = discord.Intents.default()
intents.message_content = True  # 메시지 콘텐츠 인텐트 사용

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info("✅ Logged in as %s (id: %s)", bot.user, bot.user.id)
    try:
        synced = await bot.tree.sync()
        logging.info("✅ Synced %d slash commands", len(synced))
    except Exception as e:
        logging.exception("Slash command sync error: %s", e)

# 예시 슬래시 커맨드: /ping
@bot.tree.command(name="ping", description="Check bot status")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong! 🏓", ephemeral=True)

async def main():
    token = os.getenv("TOKEN")
    if not token:
        logging.error("❌ TOKEN env var missing. Set TOKEN in Render → Environment.")
        # 환경변수 없을 때 웹 서버만 살아있게 대기
        while True:
            await asyncio.sleep(60)

    # 웹 서버 먼저 살려서 Render 포트 체크 통과
    keep_alive()

    # 실제 봇 실행
    try:
        await bot.start(token)
    except Exception as e:
        logging.exception("Bot start failed: %s", e)
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
