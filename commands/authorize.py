import discord
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
    bot_user: discord.User = kwargs["bot_user"]

    mentioned = False
    if message.role_mentions:
        mentioned = True
        for role in message.role_mentions:
            if config.add_authorized_role_to_server(role.id, message.guild.id):
                await message.channel.send(role.name + " has been added as an authorized role.")
            else:
                await message.channel.send(role.name + " is already an authorized role.")
    if message.mentions:
        for user in message.mentions:
            if user != bot_user:
                mentioned = True
                if config.add_authorized_user_to_server(user.id, message.guild.id):
                    await message.channel.send(user.display_name + " has been added as an authorized user.")
                else:
                    await message.channel.send(user.display_name + " is already authorized.")
    if not mentioned:
        await message.channel.send("You must mention the role or user you would like to authorize (with @).")
