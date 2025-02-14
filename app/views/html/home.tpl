<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="static/img/icon_estrela.png" />
    <title>FAVORITES</title>
    <!-- Link para Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../static/css/home.css">
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

<section class="hero">
    <h2>Recomendações de Anime e muito mais!!!</h2>
    <p>Milhares de histórias esperando por você. Entre, leia e compartilhe também!</p>
    <a href="/create">
       <button type="button">Cadastrar-se</button>
    </a>
</section>

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

<script src="../static/js/home.js"></script>

</body>
</html>
