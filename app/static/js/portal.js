document.addEventListener('DOMContentLoaded', () => {
    // Verificar e aplicar o tema salvo no localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        document.body.classList.remove('light-theme');
    } else {
        document.body.classList.add('light-theme');
        document.body.classList.remove('dark-theme');
    }

    // Função para alternar entre temas claro e escuro
    const toggleButton = document.getElementById('toggle-theme');
    toggleButton.addEventListener('click', () => {
        const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';

        if (currentTheme === 'dark') {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        }
    });
});

// WebSocket
const socket = io('http://localhost:8080');

// Exibir mensagem animada após login
function showAnimatedMessage(message) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("animated-message");
    messageDiv.innerText = message;
    document.body.appendChild(messageDiv);

    // Remove a mensagem após 2 segundos (depois da animação)
    setTimeout(() => {
        document.body.removeChild(messageDiv);
    }, 2000);
}

document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.querySelector("form");
    const loginButton = document.getElementById("setUsers");

    // WebSocket Login
    if (loginForm && loginButton) {
        loginButton.addEventListener("click", (event) => {
            const usernameInput = document.getElementById("username").value.trim();

            if (usernameInput) {
                socket.emit("login", { username: usernameInput });
                console.log("Login anunciado via WebSocket");
                showAnimatedMessage("Login anunciado");
            }
        });
    } else {
        console.error("Erro: Formulário ou botão de login não encontrados.");
    }
});
