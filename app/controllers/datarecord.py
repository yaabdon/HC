from app.models.user_account import UserAccount, SuperAccount
from app.models.user_message import UserMessage
from app.models.user_story import UserStory
from datetime import datetime
import json
import uuid


class StoryRecord:
    """Banco de dados JSON para o recurso: HISTÓRIAS"""
    
    def __init__(self):
        self.__user_stories = []
        self.read()  # Lê as histórias do arquivo JSON ao iniciar

    def read(self):
        """Lê as histórias do arquivo JSON e carrega no atributo user_stories"""
        try:
            with open("app/controllers/db/user_stories.json", "r") as fjson:
                user_story = json.load(fjson)
                self.__user_stories = [UserStory(**data) for data in user_story]
        except FileNotFoundError:
            print("Não existe essa história na sua biblioteca!")

    def _write(self):
        """Grava as histórias no arquivo JSON"""
        with open("app/controllers/db/user_stories.json", "w") as fjson:
            # Converte as histórias para um formato que pode ser salvo em JSON
            json.dump([story.to_dict() for story in self.__user_stories], fjson)

    def save(self, title, content, author, user):
        """Permite ao usuário salvar sua história"""
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_story = UserStory(title, content, author, creation_date)
        self.__user_stories.append(new_story)
        self._write()  # Salva a história no arquivo JSON

        user.saved_stories.append(title)
        return new_story  # Retorna a história que o usuário acabou de criar

    """def notify_users_about_new_story(self, new_story):
        for user in self.get_user_with_story(new_story.title):
            self.sio.emit('new_story_in_library', {
                'title': new_story.title,
                'author': new_story.author,
                'content': new_story.content,
                'user': user.username
            }, room=user.sid)"""

    """def get_user_with_story(self, title):
        users_with_story = []

        for user in self.__users.getAuthenticatedUsers().values():
            if title in user.saved_stories:
                users_with_story.append(user)
        return users_with_story"""
    
    def get_user_history(self, title):
        """Permite ao usuário pegar uma história pelo título"""
        for story in self.__user_stories:
            if story.title == title:
                return vars(story)  # Retorna a história em formato de dicionário
        return None  # Se não encontrar a história

    def list_user_stories(self):
        """Lista todas as histórias armazenadas"""
        return [story.title for story in self.__user_stories]

# ------------------------------------------------------------------------------

class UserRecord():
    """Banco de dados JSON para o recurso: Usuário"""

    def __init__(self):
        self.__allusers= {'user_accounts': [], 'super_accounts': []}
        self.__authenticated_users = {}
        self.read('user_accounts')
        self.read('super_accounts')


    def read(self, database):
        account_class = SuperAccount if (database == 'super_accounts') else UserAccount
        try:
            with open(f"app/controllers/db/{database}.json", "r") as fjson:
                user_d = json.load(fjson)
                self.__allusers[database] = [account_class(**data) for data in user_d]
        except FileNotFoundError:
            if database == 'super_accounts':
                self.__allusers[database] = [account_class('Guest', '000000', 'user')]  # SuperAccount com permissions
            else:
                self.__allusers[database] = [account_class('Guest', '000000')]  # UserAccount sem permissions


    def __write(self,database):
        try:
            with open(f"app/controllers/db/{database}.json", "w") as fjson:
                user_data = [vars(user_account) for user_account in \
                self.__allusers[database]]
                json.dump(user_data, fjson)
                print(f'Arquivo gravado com sucesso (Usuário)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Usuário)!')

    def getUserByUsername(self, username):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if user.username == username:
                    return user
            return None

    def setUser(self,username,password):
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:
                if username == user.username:
                    user.password= password
                    print(f'O usuário {username} foi editado com sucesso.')
                    self.__write(account_type)
                    return username
        print('O método setUser foi chamado, porém sem sucesso.')
        return None


    def removeUser(self, user):
        for account_type in ['user_accounts', 'super_accounts']:
            if user in self.__allusers[account_type]:
                print(f'O usuário {"(super) " if account_type == "super_accounts" else ""}{user.username} foi encontrado no cadastro.')
                self.__allusers[account_type].remove(user)
                print(f'O usuário {"(super) " if account_type == "super_accounts" else ""}{user.username} foi removido do cadastro.')
                self.__write(account_type)
                return user.username
        print(f'O usuário {user.username} não foi identificado!')
        return None


    def book(self, username, password, permissions):
        account_type = 'super_accounts' if permissions else 'user_accounts'
        account_class = SuperAccount if permissions else UserAccount
        new_user = account_class(username, password, permissions) if permissions else account_class(username, password)
        self.__allusers[account_type].append(new_user)
        self.__write(account_type)
        return new_user.username


    def getUserAccounts(self):
        return self.__allusers['user_accounts']


    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getAuthenticatedUsers(self):
        return self.__authenticated_users


    def checkUser(self, username, password):
        username = username.strip().lower()  # Remove espaços e converte para minúsculas
        password = password.strip()  # Remove espaços da senha
    
        for account_type in ['user_accounts', 'super_accounts']:
            for user in self.__allusers[account_type]:

                print(f"Verificando usuário: {user.username}")

                if user.username.lower() == username and user.password == password:
                    session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                    self.__authenticated_users[session_id] = user
                    print(f"Usuário autenticado: {user.username}, Session ID: {session_id}")
                    return session_id  # Retorna o ID de sessão para o usuário
        print("Falha na autenticação!")
        return None
    



    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado

#--------------------------------------------------------------------------------------------

class MessageRecord():
    """Banco de dados JSON para o recurso: Mensagem"""

    def __init__(self):
        self.__user_messages= []
        self.read()


    def read(self):
        try:
            with open("app/controllers/db/user_messages.json", "r") as fjson:
                user_msg = json.load(fjson)
                self.__user_messages = [UserMessage(**msg) for msg in user_msg]
        except FileNotFoundError:
            print('Não existem mensagens registradas!')


    def __write(self):
        try:
            with open("app/controllers/db/user_messages.json", "w") as fjson:
                user_msg = [vars(user_msg) for user_msg in \
                self.__user_messages]
                json.dump(user_msg, fjson)
                print(f'Arquivo gravado com sucesso (Mensagem)!')
        except FileNotFoundError:
            print('O sistema não conseguiu gravar o arquivo (Mensagem)!')


    def book(self,username,content):
        new_msg= UserMessage(username,content)
        self.__user_messages.append(new_msg)
        self.__write()
        return new_msg


    def getUsersMessages(self):
        return self.__user_messages

