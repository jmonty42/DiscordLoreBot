import discord
from typing import List
from objects.command import Command
from util.config import Config


async def who(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]

    command_list: List[Command] = kwargs["command_list"]
    command_set = {command.name for command in command_list}

    config: Config = kwargs["config"]

    commands_in_message = set()
    who_mentions = 0
    for word in message.content.split():
        if word in command_set:
            if word == "who":
                who_mentions += 1
                if who_mentions == 2:
                    commands_in_message.add(word)
            else:
                commands_in_message.add(word)

    if not commands_in_message:
        await message.channel.send("Please include a command to see who is authorized to use it.")

    for command in commands_in_message:
        if command == "list" or command == "who":
            await message.channel.send("Everyone can use the " + command + " command.")
        else:
            authorized_roles = config.get_authorized_roles_for_server(message.guild.id, command)
            authorized_users = config.get_authorized_users_for_server(message.guild.id, command)
            if not authorized_users and not authorized_roles:
                await message.channel.send("No permissions are set yet, so everyone can use all commands.")
                break
            role_names = [message.guild.get_role(role_id).name for role_id in authorized_roles
                          if message.guild.get_role(role_id)]
            user_names = [message.guild.get_member(user_id).display_name for user_id in authorized_users
                          if message.guild.get_member(user_id)]
            response_text = "There are no specific permissions for the " + command + " command, so the authorized " + \
                "users and roles are derived from the default permissions for this server.\n" if \
                not config.specific_authorizations_on_server_for_command(message.guild.id, command) else ""
            roles_text = "The roles that can use the " + command + " command are: " + ', '.join(role_names) + ".\n" if \
                role_names else "No roles are authorized to use the " + command + " command.\n"
            users_text = "The users that can use the " + command + " command are: " + ', '.join(user_names) + ".\n" if \
                user_names else "No users are explicitly authorized to use the " + command + " command.\n"
            await message.channel.send(''.join([response_text, roles_text, users_text]))
