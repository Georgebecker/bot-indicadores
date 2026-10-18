"""Configuração lida de variáveis de ambiente.

Nenhum valor de token vive em arquivo: a chave existe apenas na variável de
ambiente do usuário do Windows (ver AGENTS.md).
"""

from __future__ import annotations

import os
from typing import Mapping

NOME_VARIAVEL_TOKEN = "TELEGRAM_BOT_TOKEN"

URL_SGS_PADRAO = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/{quantidade}"
)


class ErroConfiguracao(Exception):
    """Configuração ausente ou inválida impede o bot de iniciar."""


def obter_token(ambiente: Mapping[str, str] | None = None) -> str:
    """Lê o token do bot e falha cedo, com mensagem clara, se ele não existir."""
    ambiente = os.environ if ambiente is None else ambiente
    token = (ambiente.get(NOME_VARIAVEL_TOKEN) or "").strip()
    if not token:
        raise ErroConfiguracao(
            f"{NOME_VARIAVEL_TOKEN} não está definida. "
            "Defina a variável de ambiente do usuário "
            "(_copilot\\scripts\\segredos.ps1 -Definir TELEGRAM_BOT_TOKEN) e reabra o terminal."
        )
    if ":" not in token or token.startswith(":") or token.endswith(":"):
        raise ErroConfiguracao(
            f"{NOME_VARIAVEL_TOKEN} não parece um token válido do BotFather "
            "(formato esperado: <números>:<texto>)."
        )
    return token
