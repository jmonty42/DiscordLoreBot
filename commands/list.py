import discord
from typing import List

from objects.command import Command


async def list_command(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]
    command_list: List[Command] = kwargs["command_list"]

    # TODO: consider making this a neat-looking embed
    response = ["> These are the commands I have:\n> \n"]
    for command in command_list:
        if not command.hidden:
            response.append(command.documentation)
            response.append("\n> \n")
    response.append("> More commands to come...")
    await message.channel.send(''.join(response))
