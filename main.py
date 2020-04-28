#! /usr/bin/env python3

import discord
import re
import Config
import Suggestion

GUILD_CHANNEL_NAME = "guild-names"
client = discord.Client()
config = Config.Config()


def main():
    # read in token
    token_file = open(config.TOKEN_FILE_NAME, "r")
    token = token_file.readline().rstrip()
    token_file.close()

    # read in master id
    master_file = open(config.MASTER_FILE_NAME, "r")
    config.set_matser_id(int(master_file.readline().rstrip()))
    master_file.close()
    print("My master's user id is " + str(config.get_master_id()))

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
        suggestions.append(Suggestion.Suggestion(count, message.content, url, author))
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
            if message.author.id != config.get_master_id():
                await message.channel.send("I don't answer to you!")
                return
            print("My master is talking to me on the " + message.guild.name + " server.")
            embed_match = re.search(r'embed', message.content)
            if embed_match:
                embed=discord.Embed(title="------------------ GUILD INFO ------------------",
                                    description="Welcome to Lore! Below you will find all major guild information or \
                                     at least where to find it.", color=0x008000, type="rich")
                embed.set_author(name="Rhino?#3873",
                                 icon_url="https://i.pinimg.com/originals/bd/19/17/bd19171b187a13f54e70c7384a1f0a4f.jpg")
                embed.add_field(name="Sixty Upgrades", value="Go to the #sixtyupgrades channel and follow the \
                                                             instructions there.", inline=False)
                embed.add_field(name="Guild Bank", value="Gb Toon: Lorebank", inline=False)
                embed.add_field(name="https://classicguildbank.com/#/guild/readonly/qlMT6AqHXUOeewBll2gycw",
                                value="This will show you what is in our guild bank. Talk to Hugsnotdrugs to request \
                                 items.", inline=False)
                embed.add_field(name="Raid Logs", value="https://classic.warcraftlogs.com/", inline=True)
                embed.add_field(name="\U0000FEFF", value="Create an account and reach out to @Hider with your Account name to \
                                be able to see our logs.", inline=True)
                embed.add_field(name="Required Guild Addons", value="\U0000FEFF", inline=False)
                embed.add_field(name="\U0000FEFF", value="Group/Guild Calendar for Classic: \
                                https://www.curseforge.com/wow/addons/group-calendar-for-classic", inline=False)
                embed.add_field(name="\U0000FEFF", value="RCLootCouncil Classic: \
                                https://www.curseforge.com/wow/addons/rclootcouncil-classic", inline=False)
                embed.add_field(name="\U0000FEFF", value="DBM: https://www.curseforge.com/wow/addons/deadly-boss-mods",
                                inline=False)
                embed.add_field(name="\U0000FEFF", value="Details: https://www.curseforge.com/wow/addons/details",
                                inline=False)
                embed.add_field(name="\U0000FEFF", value="\U0000FEFF", inline=False)
                embed.set_footer(text="footy text")
                await message.channel.send("testing embedded message...", embed=embed)
            else:
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


if __name__ == "__main__":
    main()
