import discord
import re
from objects.suggestion import Suggestion


async def fetch_suggestions(**kwargs):
    # TODO parameter validation
    message: discord.Message = kwargs["message"]
    match: re.Match = kwargs["match"]

    response_channel = message.channel
    max_results = 10
    if match.group(1):
        max_results = int(match.group(1))
    from_channel: discord.TextChannel = None
    if message.channel_mentions:
        if len(message.channel_mentions) != 1:
            await message.channel.send("Please specify 1 channel to get suggestions from.")
            return
        from_channel = message.channel_mentions[0]
    suggestion_channel = from_channel
    if suggestion_channel:
        print("Found the channel named " + suggestion_channel.name)
    messages = await suggestion_channel.history(limit=1000).flatten()
    print("Got messages from that channel.")
    suggestions = []
    for message in messages:
        url = ""
        if message.embeds:
            print("Found a message with embeds:")
            for embed in message.embeds:
                print("\tTitle: " + embed.title if isinstance(embed.title, str) else "(none)")
                print("\tType: " + embed.type if isinstance(embed.type, str) else "(none)")
                print("\tDescription: " + embed.description if isinstance(embed.description, str) else "(none)")
                print("\turl: " + embed.url if isinstance(embed.description, str) else "(none)")
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
