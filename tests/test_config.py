"""Testes da leitura do token de acesso.

Duas ideias para guardar deste arquivo:

1. Um erro de configuração precisa **explicar o que fazer** — e nunca mostrar o
   valor do token, senão ele vaza para a tela, para o log e para o print.
2. O bot deve parar **antes** de tentar conectar quando falta configuração.
"""

from __future__ import annotations

import pytest

from bot_indicadores.config import ErroConfiguracao, NOME_VARIAVEL_TOKEN, obter_token


def test_token_ausente_falha_com_mensagem_clara():
    """Sem token, o bot para antes de tentar conectar — e diz qual variável falta."""
    with pytest.raises(ErroConfiguracao) as erro:
        obter_token({})
    assert NOME_VARIAVEL_TOKEN in str(erro.value)


def test_token_vazio_falha():
    """Espaços em branco contam como ausência: não é token."""
    with pytest.raises(ErroConfiguracao):
        obter_token({NOME_VARIAVEL_TOKEN: "   "})


def test_token_sem_dois_pontos_falha():
    """Todo token de bot tem duas partes separadas por dois-pontos."""
    with pytest.raises(ErroConfiguracao):
        obter_token({NOME_VARIAVEL_TOKEN: "123456"})


def test_token_valido_e_devolvido_sem_espacos():
    """Espaço acidental em volta do token é removido, não causa falha."""
    assert obter_token({NOME_VARIAVEL_TOKEN: " 123456:ABC-def "}) == "123456:ABC-def"


def test_token_nunca_aparece_na_mensagem_de_erro():
    """Segurança: o valor nunca pode aparecer no texto do erro."""
    segredo = "987654:SEGREDO-QUE-NAO-PODE-VAZAR"
    with pytest.raises(ErroConfiguracao) as erro:
        obter_token({NOME_VARIAVEL_TOKEN: segredo + ":"})
    assert segredo not in str(erro.value)
