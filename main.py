#! /usr/bin/env python3
import discord

from util.command_list import initialize_command_list
from util.message_handler import *

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
command_list = initialize_command_list()
configuration: Config = None


def main():
    global configuration

    configuration = Config.config_factory()
    print("My master's user id is " + str(configuration.get_master_id()))

    configuration.save_to_file()

    client.run(configuration.get_token())


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    connected_server_ids = set()
    me = None
    LoreBot = None
    for server in client.guilds:
        connected_server_ids.add(server.id)
        print("Connected to the server \"" + server.name + "\" (id: " + str(server.id) + ")")
        if server.id not in configuration.get_servers_with_authorizations():
            print("Authorizations for this server are not in my configuration, initializing now...")
            configuration.initialize_authorizations_for_server(server.id)
        print("\tOther users on this server:")
        for user in server.members:
            print("\t\t" + user.display_name + " (id: " + str(user.id) + ")")
            if user.id == 297996211422494720:
                me = user
            if user.id == 702648426948591696: # LoreBot
                LoreBot = user
                print("\t\t\t manage_roles: " + str(user.guild_permissions.manage_roles))
        print("\tRoles on this server:")
        for role in server.roles:
            print("\t\t" + role.name + " (id: " + str(role.id) + ")")
            if role.id == 608347685849661480:
                for member in role.members:
                    print("\t\t\t" + member.display_name + " (" + member.name + ")")
        print("\tVoice channels on this server:")
        for channel in server.voice_channels:
            #     new_permissions = discord.PermissionOverwrite(
            #         connect = True,
            #         manage_channels = True,
            #         manage_permissions = True,
            #         speak = True,
            #         view_channel = True,
            #     )
            #     await channel.set_permissions(me, overwrite=new_permissions)
            print("\t\t" + channel.name + " (id: " + str(channel.id) + "):")
            if channel.permissions_for(LoreBot).manage_roles:
                print("\t\t\tI can manage roles here.")
            else:
                print("\t\t\tI CAN'T manage roles here.")
            for member in channel.members:
                print("\t\t\t" + member.display_name + " (" + member.name + ")")
    disconnected_server_ids = configuration.get_servers_with_authorizations() - connected_server_ids
    for disconnected_server_id in disconnected_server_ids:
        print("I am no longer a part of the server with the id: " + str(disconnected_server_id))
        print("Removing configured authorizations for that server.")
        configuration.delete_authorizations_for_server(disconnected_server_id)
    await client.close()


@client.event
async def on_guild_join(guild):
    print("I have been added to the server '" + guild.name + "' (id: " + str(guild.id) + ")")
    print("Initializing authorizations for this server.")
    configuration.initialize_authorizations_for_server(guild.id)


@client.event
async def on_guild_remove(guild):
    print("I have been removed from the server '" + guild.name + "' (id: " + str(guild.id) + ")")
    print("Deleting authorizations for this server.")
    configuration.delete_authorizations_for_server(guild.id)


@client.event
async def on_message(message):
    await handle_message(message, client, configuration, command_list)

if __name__ == "__main__":
    main()
