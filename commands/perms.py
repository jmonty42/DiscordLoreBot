import discord


async def perms(**kwargs):
    message: discord.Message = kwargs["message"]
    cos_role: discord.Role = message.guild.get_role(702554430779818074)
    cos_permissions: discord.permissions = cos_role.permissions
    print("add_reactions: " + str(cos_permissions.add_reactions))
    print("administrator: " + str(cos_permissions.administrator))
    print("attach_files: " + str(cos_permissions.attach_files))
    print("ban_members: " + str(cos_permissions.ban_members))
    print("change_nickname: " + str(cos_permissions.change_nickname))
    print("connect: " + str(cos_permissions.connect))
    print("create_instant_invite: " + str(cos_permissions.create_instant_invite))
    print("deafen_members: " + str(cos_permissions.deafen_members))
    print("embed_links: " + str(cos_permissions.embed_links))
    print("external_emojis: " + str(cos_permissions.external_emojis))
    print("kick_members: " + str(cos_permissions.kick_members))
    print("manage_channels: " + str(cos_permissions.manage_channels))
    print("manage_guild: " + str(cos_permissions.manage_guild))
    print("manage_messages: " + str(cos_permissions.manage_messages))
    print("manage_permissions: " + str(cos_permissions.manage_permissions))
    print("manage_roles: " + str(cos_permissions.manage_roles))
    print("view_audit_log: " + str(cos_permissions.view_audit_log))
    cos_permissions.create_instant_invite = True
    cos_permissions.view_audit_log = True
    cos_permissions.manage_roles = True
    #await cos_role.edit(permissions=cos_permissions, reason="Making it so that CoS can invite others and give them the role of CoS.", position=1)
    friends_role: discord.Role = message.guild.get_role(709514172664119367)
    pug_role: discord.Role = message.guild.get_role(798287141809553489)
    recruit_role: discord.Role = message.guild.get_role(608348167372537898)
    guildy_role: discord.Role = message.guild.get_role(841447638787948574)
    member_role: discord.Role = message.guild.get_role(608347976544288778)
    #await member_role.edit(position=7)
    positions = {
        friends_role: 3,
        pug_role: 4,
        recruit_role: 5,
        guildy_role: 6,
        member_role: 7
    }
    #await message.guild.edit_role_positions(positions, reason="Shifting a couple roles to lower positions")
    user: discord.Member = message.author
    if user.id == 297996211422494720:
        priest_role: discord.Role = message.guild.get_role(704058982590840953)
        #await user.remove_roles(priest_role, reason="He ain't no fuckin priest anymore")
    return
