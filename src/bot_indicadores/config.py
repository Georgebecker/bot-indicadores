"""Configuração do bot: onde ficam o token e os endereços que usamos.

Regra de segurança deste projeto (não é sugestão, é regra):
**nenhum arquivo guarda valor de chave**. O token do bot vive apenas na variável de
ambiente do usuário do Windows — como um bilhete preso na parede da sala, e não
escrito dentro do caderno que todo mundo pode folhear.

Se este arquivo guardasse o token, ele iria junto no upload para o GitHub.
Por isso, aqui só lemos o valor que já está no ambiente do sistema.
"""

from __future__ import annotations

import os
from typing import Mapping

# Nome da variável de ambiente onde o token precisa estar.
# "Variável de ambiente" é um valor que o sistema operacional guarda para o usuário.
NOME_VARIAVEL_TOKEN = "TELEGRAM_BOT_TOKEN"

# Endereço da API do Banco Central usada para buscar uma série de números.
# Os `{}` são espaços que serão preenchidos depois:
#   {codigo}     -> número da série (por exemplo, 432 é a Selic)
#   {quantidade} -> quantos valores queremos (por exemplo, os 12 últimos)
URL_SGS_PADRAO = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/{quantidade}"
)


class ErroConfiguracao(Exception):
    """Erro de configuração: falta algo para o bot conseguir começar.

    Criamos um erro com nome próprio para deixar claro, no código e na mensagem,
    que o problema é de ajuste (falta o token) e não de programação.
    """


def obter_token(ambiente: Mapping[str, str] | None = None) -> str:
    """Devolve o token do bot — ou explica com calma por que não deu.

    Pense no token como a matrícula do bot: sem ela, o Telegram não sabe quem é
    quem. Se o token estiver faltando, é melhor avisar na hora do que tentar
    conectar e falhar de um jeito confuso.

    O parâmetro `ambiente` existe para podermos testar sem mexer nas variáveis
    reais da máquina.
    """
    # Se ninguém passou um ambiente, usamos o ambiente real do sistema.
    ambiente = os.environ if ambiente is None else ambiente

    # `.get(...)` devolve None quando o nome não existe.
    # `or ""` transforma esse None em texto vazio, e `.strip()` tira espaços sobrando.
    token = (ambiente.get(NOME_VARIAVEL_TOKEN) or "").strip()

    if not token:
        # A mensagem ensina o que fazer, passo a passo. Nada de "erro 401" solto.
        raise ErroConfiguracao(
            f"{NOME_VARIAVEL_TOKEN} não está definida. "
            "Defina a variável de ambiente do usuário "
            "(_copilot\\scripts\\segredos.ps1 -Definir TELEGRAM_BOT_TOKEN) e reabra o terminal."
        )

    # Um token de bot tem sempre duas partes separadas por dois-pontos,
    # algo como 123456789:ABCdef... Se não tiver, é quase certo que houve erro de cópia.
    if ":" not in token or token.startswith(":") or token.endswith(":"):
        raise ErroConfiguracao(
            f"{NOME_VARIAVEL_TOKEN} não parece um token válido do BotFather "
            "(formato esperado: <números>:<texto>)."
        )

    # Repare que em nenhum momento imprimimos o token em mensagem de erro.
    return token
