#! /usr/bin/env python3

from util.command_list import initialize_command_list
from util.message_handler import *

client = discord.Client()
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
    for server in client.guilds:
        connected_server_ids.add(server.id)
        print("Connected to the server \"" + server.name + "\" (id: " + str(server.id) + ")")
        if server.id not in configuration.get_servers_with_authorizations():
            print("Authorizations for this server are not in my configuration, initializing now...")
            configuration.initialize_authorizations_for_server(server.id)
        print("\tOther users on this server:")
        for user in server.members:
            print("\t\t" + user.display_name + " (id: " + str(user.id) + ")")
        print("\tRoles on this server:")
        for role in server.roles:
            print("\t\t" + role.name + " (id: " + str(role.id) + ")")
    disconnected_server_ids = configuration.get_servers_with_authorizations() - connected_server_ids
    for disconnected_server_id in disconnected_server_ids:
        print("I am no longer a part of the server with the id: " + str(disconnected_server_id))
        print("Removing configured authorizations for that server.")
        configuration.delete_authorizations_for_server(disconnected_server_id)


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
