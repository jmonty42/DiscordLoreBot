import discord
from util.config import Config


async def unauthorize(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]
    config: Config = kwargs["config"]
    bot_user: discord.User = kwargs["bot_user"]

    mentioned = False
    if message.role_mentions:
        mentioned = True
        for role in message.role_mentions:
            if config.delete_authorized_role_from_server(role.id, message.guild.id):
                await message.channel.send(role.name + " has been removed as an authorized role.")
            else:
                await message.channel.send(role.name + " was not an authorized role.")
    if message.mentions:
        for user in message.mentions:
            if user != bot_user:
                mentioned = True
                if config.delete_authorized_user_from_server(user.id, message.guild.id):
                    await message.channel.send(user.display_name + " has been removed as an authorized user.")
                else:
                    await message.channel.send(user.display_name + " was not authorized.")
    if not mentioned:
        await message.channel.send("You must mention the role or user you would like to unauthorize (with @).")
