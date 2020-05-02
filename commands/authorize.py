async def authorize(message, config, bot_user):
    mentioned = False
    changed = False
    if message.role_mentions:
        mentioned = True
        for role in message.role_mentions:
            if config.add_authorized_role_id(role.id):
                await message.channel.send(role.name + " has been added as an authorized role.")
                changed = True
            else:
                await message.channel.send(role.name + " is already an authorized role.")
    if message.mentions:
        for user in message.mentions:
            if user != bot_user:
                mentioned = True
                if config.add_authorized_user_id(user.id):
                    await message.channel.send(user.display_name + " has been added as an authorized user.")
                    changed = True
                else:
                    await message.channel.send(user.display_name + " is already authorized.")
    if not mentioned:
        await message.channel.send("You must mention the role or user you would like to authorize (with @).")
    if changed:
        config.save_to_file()
