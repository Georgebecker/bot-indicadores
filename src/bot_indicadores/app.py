"""Monta o bot e o coloca para funcionar.

Dois conceitos que aparecem aqui:

**Aplicação (Application)**: é o "corpo" do bot. Ela guarda o token, sabe conversar
com o Telegram e mantém a lista de comandos.

**Polling**: em vez de o Telegram bater na nossa porta (webhook), o bot pergunta de
tempo em tempo: "tem mensagem nova para mim?". É mais simples de rodar em casa,
porque não precisa de endereço público na internet.
"""

from __future__ import annotations

import logging
import sys

from telegram.ext import Application, CommandHandler

from .bcb import ClienteSGS
from .config import ErroConfiguracao, obter_token
from .handlers import ComandosIndicadores


def criar_aplicacao(token: str, cliente: ClienteSGS | None = None) -> Application:
    """Cria o bot e liga cada comando à sua função de resposta.

    O `cliente` é opcional para os testes poderem passar um Banco Central de mentira.
    """
    # O atendente precisa saber buscar números; se ninguém passou um cliente,
    # criamos o de verdade, que fala com a internet.
    comandos = ComandosIndicadores(cliente or ClienteSGS())

    # Aqui transformamos o texto do token em uma aplicação que sabe falar Telegram.
    aplicacao = Application.builder().token(token).build()

    # Cada linha diz: "quando alguém escrever X, chame esta função".
    aplicacao.add_handler(CommandHandler("start", comandos.start))
    aplicacao.add_handler(CommandHandler("dolar", comandos.dolar))
    aplicacao.add_handler(CommandHandler("selic", comandos.selic))
    aplicacao.add_handler(CommandHandler("ipca", comandos.ipca))
    aplicacao.add_handler(CommandHandler("poupanca", comandos.poupanca))
    return aplicacao


def main() -> int:
    """Ponto de entrada: confere o token, monta o bot e fica escutando.

    Devolve 0 quando termina normalmente e 1 quando falta configuração.
    """
    # Configura o caderno de anotações: cada linha terá hora, gravidade e origem.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # Cuidado número 1: verificar o token ANTES de tentar conectar.
    # Assim o erro aparece na hora, com explicação, em vez de uma falha confusa.
    try:
        token = obter_token()
    except ErroConfiguracao as erro:
        # stderr é o canal de mensagens de erro (o "aviso" da tela).
        print(f"[configuração] {erro}", file=sys.stderr)
        return 1

    aplicacao = criar_aplicacao(token)
    logging.getLogger(__name__).info("bot iniciado em modo polling; Ctrl+C para parar")

    # `run_polling` fica rodando até alguém apertar Ctrl+C.
    aplicacao.run_polling()
    return 0
