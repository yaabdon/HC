import sys
import os

# Adiciona o diretório principal ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.controllers.application import Application

app = Application()  # Cria uma instância do seu sistema
user = app.getCurrentUserBySessionId()
print("Usuário retornado:", user) 


""""
Houve teste de cookies no site dentro do domínio e testando o código:

import sys
import os

# Adiciona o diretório principal ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.controllers.application import Application

app = Application()  # Cria uma instância do seu sistema
user = app.getCurrentUserBySessionId()
print("Usuário retornado:", user) 


Vemos que aparece none: O método não está encontrando um usuário VÁLIDO!!!!!
"""