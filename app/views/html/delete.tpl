<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="static/img/icon_estrela.png" />
    <title>FAVORITES</title>
    <!-- Link para Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../static/css/delete.css">
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

% if user:
    <h1>Página de remoção de Usuários:</h1>
    <h4>Usuário logado: {{ user.username }} </h4>
    <form action="/delete" method="post">
        <div class="button-container">
            <!-- Botão para o usuário comum remover a própria conta -->
            <input type="hidden" name="username" value="{{ user.username }}" />
            <input value="Remover minha conta" type="submit" />
        </div>
    </form>
    
    <form action="/logout" method="post">
        <button type="submit">Logout</button>
    </form>
    <form action="/portal" method="get">
        <button type="submit">Portal</button>
    </form>
    
    % if user.isAdmin():
        <h4>Como super usuário, você pode remover qualquer um dos usuários cadastrados:</h4>
        <div id="usersDisplay">
            % for member in accounts:
                <form action="/delete" method="POST">
                    <input type="hidden" name="username" value="{{ member.username }}" />
                    <button type="submit">Remover {{ member.username }}</button>
                </form>
            % end
        </div>
    % end
% else:
    <h1>Página reservada!</h1>
    <h3>Realize seu LOGIN em nosso portal</h3>
    <form action="/portal" method="get">
        <button type="submit">Portal</button>
    </form>
% end

<footer>
    <p>&copy; 2025 BOOKIES - Todos os direitos reservados</p>
</footer>

<script src="../static/js/delete.js"></script>

</body>
</html>