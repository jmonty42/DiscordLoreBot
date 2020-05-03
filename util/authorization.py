import discord
from util.config import Config


def is_user_authorized_on_server(user: discord.Member, server: discord.Guild, config: Config):
    user_id = user.id
    server_id = server.id
    if user_id in config.get_authorized_users_for_server(server_id) or user_id == config.get_master_id():
        return True
    authorized_roles = config.get_authorized_roles_for_server(server_id)
    for role in user.roles:
        if role.id in authorized_roles:
            return True
    if not config.get_authorized_users_for_server(server_id) and not authorized_roles:
        # no authorizations, default to @everyone being authorized
        return True
    return False
