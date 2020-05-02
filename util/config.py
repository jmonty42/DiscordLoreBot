import yaml


class Config:
    TOKEN_FILE_NAME = "token.txt"
    MASTER_FILE_NAME = "master.txt"
    CONFIG_YAML_FILE_NAME = "config.yml"
    SUGGESTION_CHANNEL_NAME = "guild-names"

    def __init__(self):
        self.master_id = ""
        self.token = ""
        self.authorized_user_ids = set()
        self.authorized_roles = set()

    def set_master_id(self, id):
        self.master_id = id

    def get_master_id(self):
        return self.master_id

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def add_authorized_user_id(self, id):
        if id in self.authorized_user_ids:
            return False
        self.authorized_user_ids.add(id)
        return True

    def delete_authorized_user_id(self, id):
        if id in self.authorized_user_ids:
            self.authorized_user_ids.remove(id)
            return True
        return False

    def get_authorized_user_ids(self):
        return self.authorized_user_ids

    def add_authorized_role_id(self, id):
        if id in self.authorized_roles:
            return False
        self.authorized_roles.add(id)
        return True

    def delete_authorized_role_id(self, id):
        if id in self.authorized_roles:
            self.authorized_roles.remove(id)
            return True
        return False

    def get_authorized_roles(self):
        return self.authorized_roles

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
