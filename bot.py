"""Main Bot class."""
import discord
from discord import Message
import dice

class Bot(discord.Bot):
    """The discord Bot subclass.
    """
    async def on_ready(self) -> None:
        """The event that runs when the bot gets ready.
        """
        print(f"{self.user} is ready!")

    async def on_message(self, message: Message) -> None:
        """The event thar runs when a message is sent.

        Args:
            message (Message): The Message object.
        """
        if message.author == self.user:
            return

        if roll_result := dice.get_roll_from_message(message.content):
            await message.reply(roll_result)

        print(f"{message.author}: {message.content}")
