"""Montagem da aplicação e inicialização do polling."""

from __future__ import annotations

import logging
import sys

from telegram.ext import Application, CommandHandler

from .bcb import ClienteSGS
from .config import ErroConfiguracao, obter_token
from .handlers import ComandosIndicadores


def criar_aplicacao(token: str, cliente: ClienteSGS | None = None) -> Application:
    """Cria a Application com os quatro comandos do escopo."""
    comandos = ComandosIndicadores(cliente or ClienteSGS())
    aplicacao = Application.builder().token(token).build()
    aplicacao.add_handler(CommandHandler("start", comandos.start))
    aplicacao.add_handler(CommandHandler("dolar", comandos.dolar))
    aplicacao.add_handler(CommandHandler("selic", comandos.selic))
    aplicacao.add_handler(CommandHandler("ipca", comandos.ipca))
    aplicacao.add_handler(CommandHandler("poupanca", comandos.poupanca))
    return aplicacao


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        token = obter_token()
    except ErroConfiguracao as erro:
        print(f"[configuração] {erro}", file=sys.stderr)
        return 1

    aplicacao = criar_aplicacao(token)
    logging.getLogger(__name__).info("bot iniciado em modo polling; Ctrl+C para parar")
    aplicacao.run_polling()
    return 0
