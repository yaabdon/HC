<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="static/img/icon_estrela.png" />
    <title>>.::Portal (Login)::.</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/portal.css">
</head>
<body>
    <div class="container">
    <header>
        <div class="logo">
            <h1>FAVORITES</h1>
        </div>
        <nav>
            <ul>
                <li><a href="/home">Início</a></li>
                <li><a href="#">Histórias</a></li>
                <li><a href="/portal">Entrar</a></li>
                <li><a href="#" id="toggle-theme">Mudar Tema</a></li>
            </ul>
        </nav>
    </header>
</div>

<section class="hero">
    <h2>Pronto para começar a ler novas histórias!</h2>
    <p>Um clique em direção à aventura!</p>
</section>

    <!-- BLOCO CONDICIONAL para exibir o conteúdo de login -->
    % if username:
      <div class="object_centered">
        % if edited:
            <h4>Usuário logado: {{ username }} (editado) </h4>
        % else:
            <h4>Usuário logado: {{ username }} </h4>
        % end
          <form action="/logout" method="post">
              <button type="submit">Logout</button>
          </form>
          <form action="/edit" method="get">
              <button type="submit">Área de usuário</button>
          </form>
          <form action="/chat" method="get">
              <button type="submit">Área de mensagens</button>
          </form>
      </div>
    % else:
        % if removed is not None:
            <h4>O usuário {{ removed }} foi removido deste cadastro.</h4>
        % elif created is not None:
            <h4>O usuário {{ created }} foi criado neste cadastro.</h4>
        % end
        <div class="object_centered">
          <form action="/portal" method="post">
              <label for="username">Nome:</label>
              <input id="username" name="username" type="text" required /><br>
              <label for="password">Senha:</label>
              <input id="password" name="password" type="password" required /><br>
              </br>
              <input id="setUsers" value="Login" type="submit" />
          </form>
          <form action="/create" method="get">
              <button type="submit">Criar conta de usuário</button>
          </form>
        </div>
    % end

    <footer>
        <p>&copy; 2025 BOOKIES - Todos os direitos reservados</p>
    </footer>


    <!-- Scripts -->
    <script src="/static/js/portal.js"></script>
    % if username:
        <script src="/static/js/portal.js"></script>
    % end
</body>
</html>
