#python não estava encontrando app
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.controllers.datarecord import UserRecord, MessageRecord, StoryRecord
from bottle import template, redirect, request, response, Bottle, static_file
import socketio


class Application:

    def __init__(self):

        self.pages = {
            'portal': self.portal,
            'page': self.page,
            'cadastro': self.cadastro,
            'delete': self.delete,
            'chat': self.chat,
            'edit': self.edit,
            'home': self.home,
            'history': self.history
        }
        self.__users = UserRecord()
        self.__messages = MessageRecord()
        self.__stories = StoryRecord()

        self.edited = None
        self.removed = None
        self.created= None

        # Initialize Bottle app
        self.app = Bottle()
        self.app.TEMPLATES = 'app/views/html'
        self.setup_routes()

        # Initialize Socket.IO server
        self.sio = socketio.Server(async_mode='eventlet',
    cors_allowed_origins="*") #permitir qualquer origem
        self.setup_websocket_events()

        # Create WSGI app
        self.wsgi_app = socketio.WSGIApp(self.sio, self.app)


    # estabelecimento das rotas
    def setup_routes(self):
        @self.app.route('/static/<filepath:path>')
        def server_static(filepath):
            response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            return static_file(filepath, root='./app/static')

        @self.app.route('/icon_estrela.png')
        def favicon():
            return static_file('icon_estrela.png', root='.app/static')

        @self.app.route('/page', method='GET')
        def page_getter():
            return self.render('page')

        @self.app.route('/chat', method='GET')
        def chat_getter():
            return self.render('chat')
        
        @self.app.route('/')
        @self.app.route('/home', methods = ['GET'])
        def home_getter():
            return self.render('home')
        
        @self.app.route('/portal', method='GET')
        def portal_getter():
            return self.render('portal')

        @self.app.route('/edit', method='GET')
        def edit_getter():
            return self.render('edit')

        @self.app.route('/portal', method='POST')
        def portal_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            self.authenticate_user(username, password)

        @self.app.route('/edit', method='POST')
        def edit_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            print(username + ' sendo atualizado...')
            self.update_user(username, password)
            return self.render('edit')

        @self.app.route('/cadastro', method='GET')
        def cadastro_getter():
            return self.render('cadastro')

        @self.app.route('/cadastro', method='POST')
        def cadastro_action():
            username = request.forms.get('username')
            password = request.forms.get('password')
            self.insert_user(username, password)
            return self.render('portal')

        @self.app.route('/logout', method='POST')
        def logout_action():
            self.logout_user()
            return self.render('portal')

        @self.app.route('/delete', method='GET')
        def delete_getter():
            current_user = self.getCurrentUserBySessionId()
            if current_user:
                return self.render('delete')  # Usuário autenticado pode acessar a página
            else:
                return redirect('/portal')  # Redireciona caso não esteja logado


        @self.app.route('/delete', method='POST')
        def delete_action():
            self.delete_user()
            return self.render('portal')
        
        @self.app.route('/history', methods= ['GET'])
        def history_getter():
            current_user = self.getCurrentUserBySessionId
            if current_user:
                stories = self.__stories.list_user_stories()
                auth_users = self.__users.getAuthenticatedUsers().values() #obter os usuários autenticados
                return template('app/views/html/history', current_user=current_user, stories=stories, auth_users=auth_users)
            redirect('/portal')
        
        @self.app.route('/history', methods= ['POST'])
        def history_action():
            title = request.forms.get('title')
            author = request.forms.get('author')
            content = request.forms.get('content')

            #salvar a nova história
            new_story = self.__stories.save(title, content, author)
            #emitir a história via WebSocket para todos os clientes conectadosn
            self.sio.emit('new_story', {
                'title': new_story.title, 
                'author': new_story.author, 
                'content': new_story.content, 
                'created_at': new_story.created_at
                })
            return redirect('/history')

            

    # método controlador de acesso às páginas:
    def render(self, page, parameter=None):
        content = self.pages.get(page, self.portal)
        if not parameter:
            return content()
        return content(parameter)

    # métodos controladores de páginas
    def getAuthenticatedUsers(self):
        return self.__users.getAuthenticatedUsers()

    def getCurrentUserBySessionId(self):
        session_id = request.get_cookie('session_id')
        print("Session ID recuperado:", session_id)

        user = self.__users.getCurrentUser(session_id)
        print("Usúario encontrado:", user)

        return user
        #return self.__users.getCurrentUser(session_id)

    def cadastro(self):
        return template('app/views/html/cadastro')

    def delete(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/delete', user=current_user, accounts=user_accounts)

    def edit(self):
        current_user = self.getCurrentUserBySessionId()
        user_accounts= self.__users.getUserAccounts()
        return template('app/views/html/edit', user=current_user, accounts= user_accounts)

    def portal(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            portal_render = template('app/views/html/portal', \
            username=current_user.username, edited=self.edited, \
            removed=self.removed, created=self.created)
            self.edited = None
            self.removed= None
            self.created= None
            return portal_render
        portal_render = template('app/views/html/portal', username=None, \
        edited=self.edited, removed=self.removed, created=self.created)
        self.edited = None
        self.removed= None
        self.created= None
        return portal_render

    def page(self):
        self.update_users_list()
        current_user = self.getCurrentUserBySessionId()
        print("Usuário atual:", current_user)
        if current_user:
            return template('app/views/html/page', transfered=True, current_user=current_user)
        return template('app/views/html/page', transfered=False)

    def is_authenticated(self, username):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            return username == current_user.username
        return False

    #o session_id deve ser salvo quando o usuário faz login.
    def authenticate_user(self, username, password):
        session_id = self.__users.checkUser(username, password)
        print("Novo session_id gerado:", session_id) #DEBUG

        if session_id:
            self.logout_user() #remove qualquer sessão antiga
            response.set_cookie('session_id', session_id, httponly=True, max_age=3600) #removendo secure=True para testes locais, POIS ESTOU RODANDO EM HTTP
            print(f"Cookie session_id salvo: {session_id}")  # Debug
            redirect('/page') 
        else:
            print("Falha na autenticação!")  # Debug
            redirect('/portal')  # Redireciona para o portal em caso de falha
    
    def delete_user(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            username_to_remove = request.forms.get('username')
            # Se o usuário for um administrador, ele pode remover qualquer usuário
            if current_user.isAdmin() or current_user.username == username_to_remove:
                user_to_remove = self.__users.getUserByUsername(username_to_remove)
            
                if user_to_remove:
                    print(f"Removendo o usuário: {user_to_remove.username}")
                
                    # Desloga o usuário removido
                    if user_to_remove.username == current_user.username:
                        self.logout_user()
                
                    self.removed = self.__users.removeUser(user_to_remove)  # Remover o usuário
                
                    if self.removed:
                        print(f"Usuário {user_to_remove.username} removido com sucesso")
                    else:
                        print(f"Falha na remoção do usuário: {user_to_remove.username}")
                
                    self.update_account_list()  # Atualiza a lista de usuários após a remoção
                else:
                    print("Usuário não encontrado!")
            else:
                print("Acesso negado: Apenas administradores podem remover outros usuários.")
        else:
            print("Nenhum usuário logado para remover.")
        redirect('/portal')

    def insert_user(self, username, password):
        self.created= self.__users.book(username, password,[])
        self.update_account_list()
        redirect('/portal')

    def update_user(self, username, password):
        self.edited = self.__users.setUser(username, password)
        redirect('/portal')

    def logout_user(self):
        session_id = request.get_cookie('session_id')
        self.__users.logout(session_id)
        response.delete_cookie('session_id')
        self.update_users_list()

    def chat(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            messages = self.__messages.getUsersMessages()
            auth_users= self.__users.getAuthenticatedUsers().values()
            return template('app/views/html/chat', current_user=current_user, \
            messages=messages, auth_users=auth_users)
        redirect('/portal')

    def newMessage(self, message):
        try:
            content = message
            current_user = self.getCurrentUserBySessionId()
            return self.__messages.book(current_user.username, content)
        except UnicodeEncodeError as e:
            print(f"Encoding error: {e}")
            return "An error occurred while processing the message."
        
    def home(self):
        return template('app/views/html/home')
    
    def history(self):
        current_user = self.getCurrentUserBySessionId()
        if current_user:
            stories = self.__stories.getUsersStories()
            auth_users= self.__users.getAuthenticatedUsers().values()
            return template('app/views/html/history', current_user=current_user, \
            stories=stories, auth_users=auth_users)
        redirect('/portal')
    
    # Websocket:
    def setup_websocket_events(self):

        @self.sio.event
        async def connect(sid, environ):
            print(f'Client connected: {sid}')
            await self.sio.emit('connected', {'data': 'Connected'}, room=sid)

        @self.sio.event
        async def disconnect(sid):
            print(f'Client disconnected: {sid}')


        #EVENTO DE NOVAS HISTÓRIAS
        @self.sio.event
        def new_history(sid, data):
            print(f'Nova história!: {data["title"]}')
            self.sio.emit('new_story', data) #todos os clientes receberam a nova história

    
        
        # recebimento de solicitação de cliente para atualização das mensagens
        @self.sio.event
        def message(sid, data):
            objdata = self.newMessage(data)
            self.sio.emit('message', {'content': objdata.content, 'username': objdata.username})
    

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_users_event(sid, data):
            self.sio.emit('update_users_event', {'content': data})

        # solicitação para atualização da lista de usuários conectados. Quem faz
        # esta solicitação é o próprio controlador. Ver update_users_list()
        @self.sio.event
        def update_account_event(sid, data):
            self.sio.emit('update_account_event', {'content': data})

        
    def notify_users_about_new_story(self, new_story):
        """Notifica todos os usuários sobre uma nova história."""
        for user in self.get_users_with_story(new_story.title):
            self.sio.emit('new_story_in_library', {
                'title': new_story.title,
                'author': new_story.author,
                'content': new_story.content,
                'user': user.username
            }, room=user.sid)

    def get_users_with_story(self, title):
        """Retorna os usuários que já salvaram a história."""
        users_with_story = []

        for user in self.__users.getAuthenticatedUsers().values():
            if title in user.saved_stories:
                users_with_story.append(user)
        return users_with_story

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários LOGAR ou DESLOGAR
    # este método vai forçar esta atualização em todos os CHATS ativos. Este
    # método é chamado sempre que a rota ''
    def update_users_list(self):
        print('Atualizando a lista de usuários conectados...')
        users = self.__users.getAuthenticatedUsers()
        users_list = [{'username': user.username} for user in users.values()]
        self.sio.emit('update_users_event', {'users': users_list})

    # este método permite que o controller se comunique diretamente com todos
    # os clientes conectados. Sempre que algum usuários se removerem
    # este método vai comunicar todos os Administradores ativos.
    def update_account_list(self):
        print('Atualizando a lista de usuários cadastrados...')
        users = self.__users.getUserAccounts()
        users_list = [{'username': user.username} for user in users]
        self.sio.emit('update_account_event', {'accounts': users_list})

