import discord
import re
from commands.rank_suggestions import fetch_suggestions
from commands.send_embed import embed_test
from commands.inspect import inspect


async def handle_message(message, client, config):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("I don't support DMs yet.")
        return

    if client.user in message.mentions:
        async with message.channel.typing():
            if message.author.id != config.get_master_id():
                await message.channel.send("I don't answer to you!")
                return
            print("My master is talking to me on the " + message.guild.name + " server.")
            embed_match = re.search(r'embed', message.content)
            if embed_match:
                await embed_test(message)
                return
            top_match = re.search(r'top\s*(\d+)*', message.content)
            if top_match:
                await fetch_suggestions(message, top_match, config)
                return
            inspect_match = re.search(r'inspect', message.content)
            if inspect_match:
                await inspect(message)
                return
            print("Finished processing the message...")
            return
