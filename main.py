#! /usr/bin/env python3

import discord
import re

TOKEN_FILE_NAME = "token.txt"
MASTER_FILE_NAME = "master.txt"
GUILD_CHANNEL_NAME = "guild-names"
client = discord.Client()
master = ""


def main():
    global master
    # read in token
    token_file = open(TOKEN_FILE_NAME, "r")
    token = token_file.readline().rstrip()
    token_file.close()

    # read in master id
    master_file = open(MASTER_FILE_NAME, "r")
    master = int(master_file.readline().rstrip())
    master_file.close()
    print("My master's user id is " + str(master))

    client.run(token)


async def fetch_suggestions(server, response_channel, max_results, from_channel):
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


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    for server in client.guilds:
        print("Connected to the server \"" + server.name + "\" (id: " + str(server.id) + ")")
        print("Other users on this server:")
        for user in server.members:
            print(user.display_name + " (id: " + str(user.id) + ")")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        async with message.channel.typing():
            if message.author.id != master:
                await message.channel.send("I don't answer to you!")
                return
            print("My master is talking to me on the " + message.guild.name + " server.")
            max_results = 10
            match = re.search(r'top (\d+)', message.content)
            if match and match.group(1):
                max_results = int(match.group(1))
            from_channel = GUILD_CHANNEL_NAME
            if message.channel_mentions:
                if len(message.channel_mentions) > 1:
                    message.channel.send("Please only specify 1 channel at a time to get suggestions from.")
                    return
                from_channel = message.channel_mentions[0].name
            await fetch_suggestions(message.guild, message.channel, max_results, from_channel)


class Suggestion:
    def __init__(self, votes, name, url="", author=None):
        self.votes = votes
        self.name = name
        self.url = url
        self.author = author

    def __str__(self):
        return self.name + ": " + str(self.votes) + " votes " + self.url + " by " + str(self.author)


if __name__ == "__main__":
    main()
