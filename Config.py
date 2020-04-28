class Config:

    TOKEN_FILE_NAME = "token.txt"
    MASTER_FILE_NAME = "master.txt"

    def __init__(self):
        self.master_id = ""
        self.authorized_user_ids = set()

    def set_matser_id(self, id):
        self.master_id = id

    def get_master_id(self):
        return self.master_id

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
