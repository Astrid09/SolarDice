"""Create bot and add commands."""

import os
from dotenv import load_dotenv
from discord import ApplicationContext
from bot import Bot

load_dotenv()
DISCORD_KEY: str | None = os.environ.get("BOT_TOKEN")

bot = Bot()

@bot.slash_command(
    name="test",
    description="Returns a \"Hello World\" for testing purpose."
)
async def hello_world(ctx: ApplicationContext):
    await ctx.respond("Hello World!")

bot.run(DISCORD_KEY)
