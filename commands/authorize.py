import discord
from util.authorization import is_user_authorized_on_server
from util.config import Config


async def authorize(message: discord.Message, config: Config, bot_user: discord.User):
    if not is_user_authorized_on_server(message.author, message.guild, config):
        await message.channel.send("You are not authorized to authorize people.")
        return
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
