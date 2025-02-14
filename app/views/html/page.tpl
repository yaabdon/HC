<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="static/img/icon_estrela.png" />
    <title>cRud de usuário</title>
    <link rel="stylesheet" href="/static/css/page.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.min.js"></script> <!-- Biblioteca Socket.IO -->
</head>
<body>

<header>
    <div class="logo">
        <h1>FAVORITES</h1>
    </div>
    <nav>
        <ul>
            <li><a href="/home">Início</a></li>
            <li><a href="#">Histórias</a></li>
            <li><a href="/portal">Entrar</a></li> <!-- Estamos chamando a rota do portal para realizar login -->
            <li><a href="#" id="toggle-theme">Mudar Tema</a></li>
        </ul>
    </nav>
</header>


<!-- Sessão de Usuário -->
% if transfered:
    <section class="user-info">
        <h1>Ficamos felizes com sua chegada!</h1>
        <h2>Dados do {{ "Super" if current_user.isAdmin() else "" }} Usuário:</h2>
        <p>Username: {{current_user.username}} </p>
        <p>Password: {{current_user.password}} </p>
        <div class="button-container">
            <form action="/logout" method="post">
                <button type="submit">Logout</button>
            </form>
            <form action="/edit" method="get">
                <button type="submit">Editar usuário</button>
            </form>
            <form action="/chat" method="get">
                <button type="submit">Área de mensagens</button>
            </form>
            <form action="/portal" method="get">
                <button type="submit">Portal</button>
            </form>
            <form action="/admin" method="get">
                <button type="submit">Administração</button>
            </form>
        </div>
    </section>
% else:
    <section class="login-info">
        <h1>Você ainda não fez login :(</h1>
        <h3>Realize seu LOGIN em nosso portal</h3>
        <form action="/portal" method="get">
            <button type="submit">Portal</button>
        </form>
    </section>
% end

<!-- Seção para mensagens dinâmicas -->
<div id="message-container"></div>

<script>
    // Conectar-se ao servidor WebSocket
    const socket = io.connect('http://127.0.0.1:8080');  // Endereço do servidor

    // Escutar o evento 'connected' enviado pelo servidor
    socket.on('connected', (data) => {
        console.log('Evento connected recebido:', data);  // Exibe no console

        // Cria um elemento de mensagem e o adiciona ao corpo da página
        const messageDiv = document.createElement('div');
        messageDiv.textContent = 'Você está conectado ao servidor!';
        messageDiv.style.padding = '10px';
        messageDiv.style.backgroundColor = '#4CAF50';
        messageDiv.style.color = 'white';
        messageDiv.style.marginTop = '20px';
        messageDiv.style.textAlign = 'center';
        document.getElementById('message-container').appendChild(messageDiv);
    });

    socket.on('error', (error) => {
        console.error('Erro na conexão WebSocket:', error);
        // Feedback para o usuário em caso de erro
        const errorMessage = document.createElement('div');
        errorMessage.textContent = 'Erro ao conectar ao servidor. Tente novamente mais tarde.';
        errorMessage.style.padding = '10px';
        errorMessage.style.backgroundColor = '#F44336';
        errorMessage.style.color = 'white';
        errorMessage.style.marginTop = '20px';
        errorMessage.style.textAlign = 'center';
        document.getElementById('message-container').appendChild(errorMessage);
    });
</script>

<section class="stories">
    <h2>Os mais populares</h2>
    <div class="story-card">
        <img src="https://i.pinimg.com/736x/fb/54/43/fb54435c8624af5501bccec6c9c6d9ac.jpg" alt="Capa da História 1">
        <div class="story-info">
            <h3>Kamisama Hajimemashita</h3>
            <p>Por Julietta Suzuki</p>
            <p>Uma garota que de repente tomou o lugar de um deus...</p>
        </div>
    </div>
    <div class="story-card">
        <img src="https://i.pinimg.com/736x/dd/47/a0/dd47a06bfe2def6856afac62dab68445.jpg" alt="Capa da História 2">
        <div class="story-info">
            <h3>Sailor Moon</h3>
            <p>Por Naoko Takeuchi</p>
            <p>Uma jornada espacial sem igual, cheia de descobertas e desafios...</p>
        </div>
    </div>
    <div class="story-card">
        <img src="https://i.pinimg.com/736x/04/8b/99/048b9913d697804666fa1a88f000f4f9.jpg" alt="Capa da História 3">
        <div class="story-info">
            <h3>Boku no Hero</h3>
            <p>Por Kōhei Horikoshi</p>
            <p>As consequências de um sonho impossível...</p>
        </div>
    </div>
</section>

<footer>
    <p>&copy; 2025 BOOKIES - Todos os direitos reservados</p>
</footer>

</body>
</html>
