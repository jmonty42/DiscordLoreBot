async def authorize(message, config, bot_user):
    authorized = False
    if message.role_mentions:
        authorized = True
        for role in message.role_mentions:
            if config.add_authorized_role_id(role.id):
                await message.channel.send(role.name + " has been added as an authorized role.")
            else:
                await message.channel.send(role.name + " is already an authorized role.")
    if message.mentions:
        authorized = True
        for user in message.mentions:
            if user != bot_user:
                if config.add_authorized_user_id(user.id):
                    await message.channel.send(user.display_name + " has been added as an authorized user.")
                else:
                    await message.channel.send(user.display_name + " is already authorized.")
    if not authorized:
        await message.channel.send("You must mention the role or user you would like to authorize (with @).")
    return
