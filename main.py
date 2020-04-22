#! /usr/bin/env python3

import discord

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


if __name__ == "__main__":
    main()
