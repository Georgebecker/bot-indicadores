"""Pacote do bot de indicadores.

Um "pacote" em Python é só uma pasta com arquivos `.py` que pertencem ao mesmo assunto.
Esta pasta guarda tudo que o bot precisa para funcionar:

    config.py       -> lê o token de acesso (a "senha" do bot)
    bcb.py          -> conversa com o Banco Central (busca os números)
    formatacao.py   -> transforma números em texto bonito em português
    handlers.py     -> decide o que responder quando alguém manda /dolar, /selic...
    app.py          -> monta o bot e liga tudo
    __main__.py     -> permite rodar com "python -m bot_indicadores"

A versão abaixo serve para saber qual versão está rodando quando algo quebrar.
"""

__version__ = "1.0.0"
