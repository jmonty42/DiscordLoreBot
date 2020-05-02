import discord
import re
from commands.authorize import authorize
from commands.inspect import inspect
from commands.rank_suggestions import fetch_suggestions
from commands.send_embed import embed_test
from commands.unauthorize import unauthorize


async def handle_message(message, client, config):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("I don't support DMs yet.")
        return

    if client.user in message.mentions:
        async with message.channel.typing():
            print("Message received was:")
            print(message.content)
            if message.author.id != config.get_master_id():
                await message.channel.send("I don't answer to you!")
                return
            print("My master is talking to me on the " + message.guild.name + " server.")
            embed_match = re.search(r'\bembed', message.content)
            if embed_match:
                await embed_test(message)
                return
            top_match = re.search(r'\btop\s*(\d+)*', message.content)
            if top_match:
                await fetch_suggestions(message, top_match, config)
                return
            inspect_match = re.search(r'inspect', message.content)
            if inspect_match:
                await inspect(message)
                return
            auth_match = re.search(r'\bauthorize', message.content)
            if auth_match:
                await authorize(message, config, client.user)
                return
            unauth_match = re.search(r'\bunauthorize', message.content)
            if unauth_match:
                await unauthorize(message, config, client.user)
                return
            await message.channel.send("Sorry, I'm not sure what you want me to do.")
            print("Finished processing the message...")
        return
