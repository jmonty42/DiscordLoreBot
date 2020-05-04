import discord
from typing import List
from objects.command import Command
from util.config import Config


async def authorize(**kwargs):
    if "message" not in kwargs:
        print("Error in authorize: no message parameter given.")
        return
    message: discord.Message = kwargs["message"]
    if "config" not in kwargs:
        print("Error in authorize: no config parameter given.")
        return
    config: Config = kwargs["config"]
    if "bot_user" not in kwargs:
        print("Error in authorize: no bot_user parameter given.")
        return
    bot_user: discord.User = kwargs["bot_user"]
    if "command_list" not in kwargs:
        print("Error in authorize: no command_list parameter given.")
        return

    unauthorize = False
    if "unauthorize" in kwargs:
        unauthorize = kwargs["unauthorize"]

    command_list: List[Command] = kwargs["command_list"]
    command_set = {command.name for command in command_list}

    commands_in_message = set()
    unauthorizes_in_message = 0
    authorizes_in_message = 0
    for word in message.content.split():
        print("Checking \"" + word + "\" from message...")
        if word in command_set:
            print("This is a command word.")
            # "authorize" will appear in every message that triggers the authorize command, so the first instance needs
            # to be filtered out. Same with "unauthorize" for unauthorize commands.
            if word == "authorize" and not unauthorize:
                authorizes_in_message += 1
                if authorizes_in_message == 2:
                    commands_in_message.add(word)
                else:
                    print("Did not add it, because it was the first authorize found in an authorize command.")
            elif word == "unauthorize":
                if authorizes_in_message == 0 and not unauthorize:
                    # "unauthorize" appears before "authorize" in the message, so this is actually an unauthorize
                    # command
                    print("This authorize command is actually an unauthorize command, oops!")
                    unauthorize = True
                if unauthorize:
                    unauthorizes_in_message += 1
                    if unauthorizes_in_message == 2:
                        commands_in_message.add(word)
                else:
                    commands_in_message.add(word)
            else:
                print("Adding to the commands_in_message set")
                commands_in_message.add(word)
    print("Commands found: " + str(commands_in_message))

    mentioned = False
    if message.role_mentions:
        mentioned = True
        for role in message.role_mentions:
            if commands_in_message:
                for command in commands_in_message:
                    if unauthorize:
                        if config.delete_authorized_role_from_server(role.id, message.guild.id, command):
                            await message.channel.send(role.name + " is no longer authorized to use the "
                                                       + command + " command.")
                        else:
                            await message.channel.send(role.name + " was not authorized to use the "
                                                       + command + " command.")
                    else:
                        if config.add_authorized_role_to_server(role.id, message.guild.id, command):
                            await message.channel.send(role.name + " has been authorized to use the "
                                                       + command + " command.")
                        else:
                            await message.channel.send(role.name + " is already authorized to use the "
                                                       + command + " command.")
            else:
                if unauthorize:
                    if config.delete_authorized_role_from_server(role.id, message.guild.id):
                        await message.channel.send(role.name + " is no longer an authorized role.")
                    else:
                        await message.channel.send(role.name + " was not an authorized role.")
                else:
                    if config.add_authorized_role_to_server(role.id, message.guild.id):
                        await message.channel.send(role.name + " has been added as an authorized role.")
                    else:
                        await message.channel.send(role.name + " is already an authorized role.")
    if message.mentions:
        for user in message.mentions:
            if user != bot_user:
                mentioned = True
                if commands_in_message:
                    for command in commands_in_message:
                        if unauthorize:
                            if config.delete_authorized_user_from_server(user.id, message.guild.id, command):
                                await message.channel.send(user.display_name + " is no longer authorized to use the "
                                                           + command + " command.")
                            else:
                                await message.channel.send(user.display_name + " was not authorized to use the "
                                                           + command + " command.")
                        else:
                            if config.add_authorized_user_to_server(user.id, message.guild.id, command):
                                await message.channel.send(user.display_name + " has been authorized to use the "
                                                           + command + " command.")
                            else:
                                await message.channel.send(user.display_name + " is already authorized to use the "
                                                           + command + " command.")
                else:
                    if unauthorize:
                        if config.delete_authorized_user_from_server(user.id, message.guild.id):
                            await message.channel.send(user.display_name + " is no longer an authorized user.")
                        else:
                            await message.channel.send(user.display_name + " was not an authorized user.")
                    else:
                        if config.add_authorized_user_to_server(user.id, message.guild.id):
                            await message.channel.send(user.display_name + " has been added as an authorized user.")
                        else:
                            await message.channel.send(user.display_name + " is already authorized.")
    if not mentioned:
        if unauthorize:
            await message.channel.send("You must mention the role or user you would like to unauthorize (with @).")
        else:
            await message.channel.send("You must mention the role or user you would like to authorize (with @).")
