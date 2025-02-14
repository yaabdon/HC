class UserAccount():

    def __init__(self, username, password, saved_stories=None):
        self.username= username
        self.password= password
        self.saved_stories = saved_stories if saved_stories is not None else[] #cada instância de UserAccount e SuperAccount terá uma lista chamada saved_stories, que armazenará os títuloss das histórias que o usuário salvou.    

    def isAdmin(self):
        return False


class SuperAccount(UserAccount):

    def __init__(self, username, password, permissions, saved_stories=None):

        super().__init__(username, password)
        self.permissions = permissions if permissions else ['user']
        self.saved_stories = saved_stories if saved_stories else []
        
    def isAdmin(self):
        return True
