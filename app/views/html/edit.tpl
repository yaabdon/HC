<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="static/img/icon_estrela.png" />
    <title>crUd de usuário</title>
    <script src="/static/js/websocket/socket.io.min.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/css/edit.css">
    <script src="/static/js/edit.js"></script>
</head>
<body>
     % if user:
        <h1>Página de edição de Usuários:</h1>
        <h4>Usuário logado: {{ user.username }} </h4>
          <form action="/edit" method="post">
            <label for="username">Nome:</label>
            <input id="username" name="username" type="text"
              value="{{ user.username }}" readonly /><br>
            <label for="password">Senha:</label>
            <input id="password" name="password" type="password" required /><br>
          </br>
            <div class= "button-container">
              <input value="Editar" type="submit" />
              <form action="/logout" method="post">
                <button type="submit">Logout</button>
              </form>
              <form action="/portal" method="get">
                <button type="submit">Portal</button>
              </form>
              <form action="/delete" method="get">
                <button type="submit">Deletar usuário</button>
              </form>
            </div>
          </form>
        % if user.isAdmin():
          <h4>Como super usuário, você pode editar qualquer um dos usuários cadastrados:</h4>
         <div id="editDisplay">
             % for member in accounts:
               <li>{{ member.username }}</li>
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
</body>
</html>
