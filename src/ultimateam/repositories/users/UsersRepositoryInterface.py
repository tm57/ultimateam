from interface import Interface


class UsersRepositoryInterface(Interface):
    def create(self, email, password, passphrase):
        pass

    def getUser(self, user_id):
        pass
