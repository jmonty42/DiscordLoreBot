import discord
from time import sleep
from typing import Set


async def summon(**kwargs):
    # TODO: parameter validation
    message: discord.Message = kwargs["message"]

    author_voice_state: discord.VoiceState = message.author.voice
    if not author_voice_state or not author_voice_state.channel:
        await message.channel.send("Sorry, you're not currently in a voice channel, I can't summon for you.")
        return
    if author_voice_state.afk:
        await message.channel.send("I won't summon people to AFK.")
        return
    if message.mention_everyone:
        await message.channel.send("Being able to summon everyone is too much power for one person to wield.")
        return
    if not message.role_mentions and len(message.mentions) == 1:
        await message.channel.send("I can't summon anyone if you don't mention them.")
        return

    summon_channel = author_voice_state.channel
    # TODO: remove when this does something
    await message.channel.send("Summoning to channel " + summon_channel.name + " now!")

    requested_users: Set[discord.Member] = set(message.mentions)
    for role in message.role_mentions:
        requested_users = requested_users.union(set(role.members))

    summons = 0
    for user in requested_users:
        if not user.voice:
            continue
        if user.voice.channel == summon_channel:
            continue
        if user.voice.afk:
            continue
        attempt = 0
        max_retries = 3
        reason_string = " ".join(["Summoned by", message.author.display_name, "with LoreBot."])
        while attempt < max_retries:
            try:
                await user.move_to(summon_channel, reason=reason_string)
                summons += 1
                sleep(0.25)
                break
            except discord.Forbidden as error:
                await message.channel.send("I couldn't move " + user.display_name + " from " + user.voice.channel.name
                                           + " because I don't have the right permissions.")
                print("Got forbidden error when trying to move " + user.display_name + " from " +
                      user.voice.channel.name + " to " + summon_channel.name)
                print("Forbidden message: " + error.text)
                break
            except discord.HTTPException:
                print("Got HTTPException when trying to summon " + user.display_name)
                attempt += 1

    if summons > 0:
        await message.channel.send("Summoning complete. Did it work?")
    else:
        await message.channel.send("I didn't summon anyone, maybe they were offline or afk?")
