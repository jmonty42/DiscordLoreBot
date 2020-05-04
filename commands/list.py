import discord
from typing import List

from objects.command import Command


async def list_command(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]
    command_list: List[Command] = kwargs["command_list"]

    # TODO: consider making this a neat-looking embed
    first_line = "> These are the commands I have:"
    command_docs = [command.documentation for command in command_list if not command.hidden]
    last_line = "> More commands to come..."
    await message.channel.send("\n> \n".join([first_line, *command_docs, last_line]))
