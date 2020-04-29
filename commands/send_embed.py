import discord

async def embed_test(message):
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
