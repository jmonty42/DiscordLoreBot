#! /usr/bin/env python3

import os
import yaml
from util.config import Config
from util.message_handler import *

client = discord.Client()
configuration = None


def main():
    global configuration

    configuration = Config.config_factory()
    print("My master's user id is " + str(configuration.get_master_id()))

    if not os.path.isfile(configuration.CONFIG_YAML_FILE_NAME):
        with open(configuration.CONFIG_YAML_FILE_NAME, 'w') as config_output:
            yaml.dump(configuration, config_output)

    client.run(configuration.get_token())


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    for server in client.guilds:
        print("Connected to the server \"" + server.name + "\" (id: " + str(server.id) + ")")
        print("Other users on this server:")
        for user in server.members:
            print(user.display_name + " (id: " + str(user.id) + ")")


@client.event
async def on_message(message):
    await handle_message(message, client, configuration)

if __name__ == "__main__":
    main()
