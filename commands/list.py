import discord


async def list(message: discord.Message):
    # TODO: consider making this a neat-looking embed
    response = """These are the commands I have:
top (n)
    Finds the top n posts in the mentioned text channel based on reactions from unique users. If n is not specified, 
    it defaults to 10. This was used to vote on the guild name and tabard when we formed.
    Usage:
    @LoreBot top 5 #guild-name-suggestions
    
authorize [@user|@role] (command)
    Authorizes the mentioned user or role to use the specified command. If no command is given, it authorizes the user
    for with the default level of authorization, which is applied to commands that have not had explicit permissions
    set.
    Usage:
    @LoreBot authorize @MarkSargent top
    @LoreBot authorize @Officer
    
unauthorize [@user|@role] (command)
    Removes authorization for the mentioned user or role for the specified command or from the default level of
    authorization if no command was specified.
    Usage:
    @LoreBot unauthorize @Melkhior authorize
    @LoreBot unauthorize @Frauggs
    
More commands to come..."""
    await message.channel.send(response)
