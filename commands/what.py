import discord
from typing import List
from objects.command import Command
from util.authorization import is_user_authorized_on_server
from util.config import Config


async def what(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]

    config: Config = kwargs["config"]

    command_list: List[Command] = kwargs["command_list"]

    bot_user: discord.User = kwargs["bot_user"]

    for role in message.role_mentions:
        commands_authorized_for = [command.name for command in command_list if role.id in
                                   config.get_authorized_roles_for_server(message.guild.id, command.name) or
                                   command.name == "who" or command.name == "list"]
        # commands_authorized_for = []
        # for command in command_list:
        #    if command.name == "who" or command.name == "list":
        #        command_list.append(command.name)
        #    elif role.id in config.get_authorized_roles_for_server(message.guild.id, command.name)
        authorized_commands = ", ".join(commands_authorized_for)
        await message.channel.send(" ".join([role.name, "is authorized to use the commands:", authorized_commands]))

    for user in message.mentions:
        if user != bot_user:
            commands_authorized_for = [command.name for command in command_list if
                                       is_user_authorized_on_server(user, message.guild, config, command)]
            authorized_commands = ", ".join(commands_authorized_for)
            await message.channel.send(" ".join([user.display_name, "is authorized to use the commands:",
                                                 authorized_commands]))

    if not message.role_mentions and len(message.mentions) == 1:
        commands_authorized_for = [command.name for command in command_list if
                                   is_user_authorized_on_server(message.author, message.guild, config, command)]
        authorized_commands = ", ".join(commands_authorized_for)
        await message.channel.send(" ".join(["You didn't mention any roles or users, so here are the commands",
                                             "that you are authorize to use:", authorized_commands]))
