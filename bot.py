import os, time, asyncio
import discord
from discord.ext import commands
from aiohttp import web

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1432284030073700553

# Discord intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id={bot.user.id})")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id == CHANNEL_ID:
        await message.channel.send(
            "@everyone",
            allowed_mentions=discord.AllowedMentions(everyone=True)
        )
    await bot.process_commands(message)

# --- 아주 얇은 헬스체크 웹서버 (PaaS용) ---
async def handle_health(request):
    return web.Response(text="ok")
async def start_web_app():
    app = web.Application()
    app.router.add_get("/", handle_health)
    port = int(os.getenv("PORT", "8080"))
    runner = web.AppRunner(app); await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port); await site.start()
    print(f"🌐 Health server on :{port}")

async def main():
    # 웹서버와 디스코드 봇 동시에 실행
    await start_web_app()
    await bot.start(TOKEN)

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("환경변수 DISCORD_TOKEN이 없습니다.")
    asyncio.run(main())
