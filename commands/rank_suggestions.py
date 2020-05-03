import discord
import re
from objects.suggestion import Suggestion
from util.authorization import is_user_authorized_on_server
from util.config import Config


async def fetch_suggestions(**kwargs):
    # TODO parameter validation
    message: discord.Message = kwargs["message"]
    match: re.Match = kwargs["match"]
    config: Config = kwargs["config"]

    server = message.guild
    if not is_user_authorized_on_server(message.author, server, config):
        await message.channel.send("I don't answer to you!")
        return
    response_channel = message.channel
    max_results = 10
    if match.group(1):
        max_results = int(match.group(1))
    from_channel = config.SUGGESTION_CHANNEL_NAME
    if message.channel_mentions:
        if len(message.channel_mentions) > 1:
            await message.channel.send("Please only specify 1 channel at a time to get suggestions from.")
            return
        from_channel = message.channel_mentions[0].name
    suggestion_channel = [channel for channel in server.text_channels if channel.name == from_channel][0]
    if suggestion_channel:
        print("Found the channel named " + suggestion_channel.name)
    else:
        response_channel.send("Sorry, I couldn't find the channel named \"" + from_channel + "\"")
        return
    messages = await suggestion_channel.history(limit=1000).flatten()
    print("Got messages from that channel.")
    suggestions = []
    for message in messages:
        url = ""
        if message.embeds:
            print("Found a message with embeds:")
            for embed in message.embeds:
                print("\tTitle: " + embed.title)
                print("\tType: " + embed.type)
                print("\tDescription: " + embed.description)
                print("\turl: " + embed.url)
                print("\timage: " + str(embed.image))
                print("\tthumbnail: " + str(embed.thumbnail))
        if message.attachments:
            print("Found a message with attachments:")
            for attachment in message.attachments:
                print("\turl: " + attachment.url)
                url = attachment.url
        author = message.author
        count = 0
        voters = set()
        for reaction in message.reactions:
            if str(reaction) != "\U0001F44E":
                users = await reaction.users().flatten()
                voters_count = len(voters)
                voters = voters.union(set(users))
                count += len(voters) - voters_count
        suggestions.append(Suggestion(count, message.content, url, author))
    suggestions.sort(key=lambda suggestion: suggestion.votes, reverse=True)
    for rank in range(len(suggestions)):
        response_string = str(rank + 1) + ": from " + suggestions[rank].author.mention
        if not suggestions[rank].url:
            response_string += ": " + suggestions[rank].name
        response_string += ": (" + str(suggestions[rank].votes) + " votes)\n "

        if suggestions[rank].url:
            embed = discord.Embed(type="rich")
            embed.set_image(url=suggestions[rank].url)
            await response_channel.send(response_string, embed=embed)
        else:
            await response_channel.send(response_string)

        if rank + 1 >= max_results:
            break
    if len(suggestions) < 1:
        await response_channel.send("Something went wrong trying to get the suggestions, sorry.")
