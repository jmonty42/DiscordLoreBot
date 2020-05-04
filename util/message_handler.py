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
                print("Checking if this is a " + command.name + " command.")
                match = re.search(command.regex, message.content)
                if match:
                    if command.check_defer and should_defer(message.content, command.name,
                                                            [command.name for command in command_list]):
                        print("Thought this might be a " + command.name + " command, but there's another command " +
                              "mentioned earlier in the message, deferring.")
                        continue
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


def should_defer(message_str: str, command_name: str, other_commands: List[str]):
    command_index = message_str.find(command_name)
    for other in other_commands:
        other_index = message_str.find(other)
        if -1 < other_index < command_index:
            print(other + " comes before " + command_name + " in this message.")
            return True
    return False
