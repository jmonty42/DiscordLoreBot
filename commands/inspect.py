import discord


async def inspect(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]

    inspect_channel = message.channel
    if message.channel_mentions:
        if len(message.channel_mentions) > 1:
            await message.channel.send("Please only specify 1 channel at a time to inspect.")
            return
        inspect_channel = message.channel_mentions[0]
    async for message in inspect_channel.history(limit=20):
        print (str(message.id) + ": from " + message.author.name)
    messages = [704931310212481035, 704929763755687978, 704929069778731008, 704928607814025236, 706390995385843732,
                706390868377993237]
    for message_id in messages:
        bot_message = await message.channel.fetch_message(message_id)
        print(str(bot_message.id) + " at " + str(bot_message.created_at) + ":")
        print(bot_message.content)
        for embed in bot_message.embeds:
            if embed.title != discord.Embed.Empty:
                print("embed title: " + embed.title)
            if embed.type != discord.Embed.Empty:
                print("embed type: " + embed.type)
            if embed.description != discord.Embed.Empty:
                print("embed description: " + embed.description)
            if embed.color != discord.Embed.Empty:
                print("embed color: " + str(embed.color))
            if embed.image != discord.Embed.Empty:
                print("embed image: " + str(embed.image))
            for field in embed.fields:
                print("embed field: " + str(field))
    await message.channel.send("Check your console.")
    return
