import discord
import re
from commands.rank_suggestions import fetch_suggestions
from commands.send_embed import embed_test


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
            else:
                max_results = 10
                match = re.search(r'top (\d+)', message.content)
                if match and match.group(1):
                    max_results = int(match.group(1))
                from_channel = config.SUGGESTION_CHANNEL_NAME
                if message.channel_mentions:
                    if len(message.channel_mentions) > 1:
                        message.channel.send("Please only specify 1 channel at a time to get suggestions from.")
                        return
                    from_channel = message.channel_mentions[0].name
                await fetch_suggestions(message.guild, message.channel, max_results, from_channel)
            print("Finished processing the message...")
            return
