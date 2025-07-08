"""Create bot and add commands."""

import os
from dotenv import load_dotenv
from discord import ApplicationContext, guild_only, default_permissions
from bot import Bot

load_dotenv()
DISCORD_KEY: str | None = os.environ.get("BOT_TOKEN")
TEST_GUILD: str | None = os.environ.get("TEST_GUILD")

bot = Bot()

@bot.slash_command(
    name="test",
    description="Returns a \"Hello World\" for testing purpose.",
    guild_id=[TEST_GUILD]
)
@default_permissions(administrator=True)
@guild_only()
async def hello_world(ctx: ApplicationContext):
    await ctx.respond("Hello World!")

bot.run(DISCORD_KEY)
