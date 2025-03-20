import discord
from typing import List

async def clear(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]

    channel_list: List[discord.GuildChannel | discord.Thread] = message.channel_mentions

    if len(channel_list) != 1:
        await message.channel.send("You must specify exactly one channel to clear out.")
        return
    clear_channel: discord.TextChannel = channel_list[0]
    bot_user: discord.ClientUser = kwargs["bot_user"]
    bot_member: discord.Member = message.guild.get_member(bot_user.id)
    if not clear_channel.permissions_for(bot_member).manage_messages:
        await message.channel.send("I don't have permission to clear the messages in " + clear_channel.name + ".")
        return
    await clear_channel.purge()
    await message.channel.send("I've cleared out the messages in " + clear_channel.name + ".")
