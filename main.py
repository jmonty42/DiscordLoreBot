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


async def fetch_suggestions(server, response_channel, max=10):
    suggestion_channel = [channel for channel in server.text_channels if channel.name == GUILD_CHANNEL_NAME][0]
    print("Found the channel named " + suggestion_channel.name)
    messages = await suggestion_channel.history(limit=1000).flatten()
    print("Got messages from that channel.")
    suggestions = []
    for message in messages:
        count = 0
        for reaction in message.reactions:
            if str(reaction) != "\U0001F44E":
                count += reaction.count
        suggestions.append(Suggestion(count, message.content))
    suggestions.sort(key=lambda suggestion: suggestion.votes, reverse=True)
    response_string = ""
    for rank in range(len(suggestions)):
        response_string += str(rank+1) + ": " + suggestions[rank].name + ": (" + str(suggestions[rank].votes) \
                           + " votes)\n "
        if rank+1 >= max:
            break
    if response_string:
        await response_channel.send(response_string)
    else:
        response_channel.send("Something went wrong trying to get the suggestions, sorry.")


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        if message.author.id != master:
            await message.channel.send("I don't answer to you!")
            return
        print("My master is talking to me on the " + message.guild.name + " server.")
        max_results = 10
        match = re.search(r'top (\d+)', message.content)
        if match and match.group(1):
            max_results = int(match.group(1))
        await fetch_suggestions(message.guild, message.channel, max_results)


class Suggestion:
    def __init__(self, votes, name):
        self.votes = votes
        self.name = name

    def __str__(self):
        return self.name + ": " + str(self.votes) + " votes"


if __name__ == "__main__":
    main()
