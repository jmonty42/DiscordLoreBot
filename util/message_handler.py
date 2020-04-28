import discord
import re
from commands.rank_suggestions import fetch_suggestions


async def handle_message(message, client, config):
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
                print("Sent the embedded message...")
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
