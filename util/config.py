import yaml


class Config:
    TOKEN_FILE_NAME = "token.txt"
    MASTER_FILE_NAME = "master.txt"
    CONFIG_YAML_FILE_NAME = "config.yml"
    SUGGESTION_CHANNEL_NAME = "guild-names"
    USERS_KEY = "users"
    ROLES_KEY = "roles"

    @classmethod
    def config_factory(cls):
        try:
            with open(cls.CONFIG_YAML_FILE_NAME, 'r') as yaml_file:
                print("Initializing config from " + cls.CONFIG_YAML_FILE_NAME)
                return yaml.load(yaml_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print(cls.CONFIG_YAML_FILE_NAME + " does not exist, initializing the config without it.")
        config = cls()
        try:
            with open(cls.TOKEN_FILE_NAME, 'r') as token_file:
                config.set_token(token_file.readline().rstrip())
        except FileNotFoundError:
            print(cls.TOKEN_FILE_NAME + " does not exist, cannot initialize config.")
            raise
        try:
            with open(cls.MASTER_FILE_NAME, 'r') as master_file:
                config.set_master_id(int(master_file.readline().rstrip()))
        except FileNotFoundError:
            print(cls.MASTER_FILE_NAME + " does not exist, cannot initialize config.")
            raise
        return config

    def __init__(self):
        self.__master_id = ""
        self.__token = ""
        self.__authorizations_by_server = {}

    def save_to_file(self):
        with open(self.CONFIG_YAML_FILE_NAME, 'w') as config_output:
            yaml.dump(self, config_output)

    def set_master_id(self, master_id):
        self.__master_id = master_id

    def get_master_id(self):
        return self.__master_id

    def set_token(self, token):
        self.__token = token

    def get_token(self):
        return self.__token

    def add_authorized_user_to_server(self, user_id, server_id, command=""):
        if server_id in self.__authorizations_by_server:
            if command:
                if command not in self.__authorizations_by_server[server_id]:
                    self.__authorizations_by_server[server_id][command] = {}
                    self.__authorizations_by_server[server_id][command][self.USERS_KEY] = set()
                    self.__authorizations_by_server[server_id][command][self.ROLES_KEY] = set()
                if user_id in self.__authorizations_by_server[server_id][command][self.USERS_KEY]:
                    return False
                self.__authorizations_by_server[server_id][command][self.USERS_KEY].add(user_id)
                self.save_to_file()
                return True
            if user_id in self.__authorizations_by_server[server_id][self.USERS_KEY]:
                return False
            self.__authorizations_by_server[server_id][self.USERS_KEY].add(user_id)
            self.save_to_file()
            return True
        # TODO: throw an exception for bad server id
        return False

    def delete_authorized_user_from_server(self, user_id, server_id, command=""):
        if server_id in self.__authorizations_by_server:
            if command:
                if command not in self.__authorizations_by_server[server_id]:
                    return False
                if user_id in self.__authorizations_by_server[server_id][command][self.USERS_KEY]:
                    self.__authorizations_by_server[server_id][command][self.USERS_KEY].remove(user_id)
                    if not self.__authorizations_by_server[server_id][command][self.USERS_KEY] and \
                            not self.__authorizations_by_server[server_id][command][self.ROLES_KEY]:
                        self.__authorizations_by_server[server_id].pop(command)
                    self.save_to_file()
                    return True
                return False
            if user_id in self.__authorizations_by_server[server_id][self.USERS_KEY]:
                self.__authorizations_by_server[server_id][self.USERS_KEY].remove(user_id)
                self.save_to_file()
                return True
            return False
        # TODO: throw an exception for bad server id
        return False

    def get_authorized_users_for_server(self, server_id, command=""):
        if server_id in self.__authorizations_by_server:
            if command and command in self.__authorizations_by_server[server_id]:
                return self.__authorizations_by_server[server_id][command][self.USERS_KEY]
            return self.__authorizations_by_server[server_id][self.USERS_KEY]
        # TODO: throw an exception for bad server id
        return set()

    def add_authorized_role_to_server(self, role_id, server_id, command=""):
        if server_id in self.__authorizations_by_server:
            if command:
                if command not in self.__authorizations_by_server[server_id]:
                    self.__authorizations_by_server[server_id][command] = {}
                    self.__authorizations_by_server[server_id][command][self.USERS_KEY] = set()
                    self.__authorizations_by_server[server_id][command][self.ROLES_KEY] = set()
                if role_id in self.__authorizations_by_server[server_id][command][self.ROLES_KEY]:
                    return False
                self.__authorizations_by_server[server_id][command][self.ROLES_KEY].add(role_id)
                self.save_to_file()
                return True
            if role_id in self.__authorizations_by_server[server_id][self.ROLES_KEY]:
                return False
            self.__authorizations_by_server[server_id][self.ROLES_KEY].add(role_id)
            self.save_to_file()
            return True
        # TODO: throw an exception for bad server id
        return False

    def delete_authorized_role_from_server(self, role_id, server_id, command=""):
        if server_id in self.__authorizations_by_server:
            if command:
                if command not in self.__authorizations_by_server[server_id]:
                    return False
                if role_id in self.__authorizations_by_server[server_id][command][self.ROLES_KEY]:
                    self.__authorizations_by_server[server_id][command][self.ROLES_KEY].remove(role_id)
                    if not self.__authorizations_by_server[server_id][command][self.USERS_KEY] and \
                            not self.__authorizations_by_server[server_id][command][self.ROLES_KEY]:
                        self.__authorizations_by_server[server_id].pop(command)
                    self.save_to_file()
                    return True
                return False
            if role_id in self.__authorizations_by_server[server_id][self.ROLES_KEY]:
                self.__authorizations_by_server[server_id][self.ROLES_KEY].remove(role_id)
                self.save_to_file()
                return True
            return False
        # TODO: throw an exception for bad server id
        return False

    def get_authorized_roles_for_server(self, server_id, command=""):
        if server_id in self.__authorizations_by_server:
            if command and command in self.__authorizations_by_server[server_id]:
                return self.__authorizations_by_server[server_id][command][self.ROLES_KEY]
            return self.__authorizations_by_server[server_id][self.ROLES_KEY]
        # TODO: throw an exception for bad server id
        return set()

    def get_servers_with_authorizations(self):
        return set(self.__authorizations_by_server.keys())

    def initialize_authorizations_for_server(self, server_id):
        if server_id not in self.__authorizations_by_server:
            self.__authorizations_by_server[server_id] = {}
            self.__authorizations_by_server[server_id][self.USERS_KEY] = set()
            self.__authorizations_by_server[server_id][self.ROLES_KEY] = set()
            self.save_to_file()
        # TODO: throw an exception for bad server id

    def delete_authorizations_for_server(self, server_id):
        if server_id in self.__authorizations_by_server:
            del(self.__authorizations_by_server[server_id])
            self.save_to_file()
        # TODO: throw an exception for bad server id

    def specific_authorizations_on_server_for_command(self, server_id, command):
        if server_id in self.__authorizations_by_server:
            print(str(self.__authorizations_by_server[server_id]))
            print(command in self.__authorizations_by_server[server_id])
            return command in self.__authorizations_by_server[server_id]
        # TODO: throw an excception for bad server id
        return False

    def does_server_have_authorizations_configured(self, server_id):
        if server_id in self.__authorizations_by_server:
            user_set_empty = not self.__authorizations_by_server[server_id][self.USERS_KEY]
            role_set_empty = not self.__authorizations_by_server[server_id][self.ROLES_KEY]
            server_has_no_command_sets = len(self.__authorizations_by_server[server_id]) == 2
            if user_set_empty and role_set_empty and server_has_no_command_sets:
                print("Serve has no authorizations configured, returning False")
                return False
        return True
