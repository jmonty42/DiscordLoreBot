import discord
import re
from typing import List

from objects.command import Command
from util.authorization import is_user_authorized_on_server
from util.config import Config


async def handle_message(message: discord.Message, client: discord.Client, config: Config, command_list: List[Command]):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("I don't support DMs yet.")
        return

    if client.user in message.mentions:
        async with message.channel.typing():
            print("Message received was:")
            print(message.content)
            for command in command_list:
                match = re.search(command.regex, message.content)
                if match:
                    print("Handling message as the '" + command.name + "' command.")
                    if not is_user_authorized_on_server(message.author, message.guild, config, command):
                        response_string = command.not_authorized if command.not_authorized \
                            else "You are not authorized to do that."
                        await message.channel.send(response_string)
                        return
                    await command.method(
                        message=message,
                        config=config,
                        match=match,
                        bot_user=client.user,
                        command_list=command_list
                    )
                    return
            await message.channel.send("Sorry, I'm not sure what you want me to do.")
            print("Finished processing the message...")
        return
