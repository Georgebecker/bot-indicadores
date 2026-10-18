"""Testes de configuração e do token do bot."""

from __future__ import annotations

import pytest

from bot_indicadores.config import ErroConfiguracao, NOME_VARIAVEL_TOKEN, obter_token


def test_token_ausente_falha_com_mensagem_clara():
    with pytest.raises(ErroConfiguracao) as erro:
        obter_token({})
    assert NOME_VARIAVEL_TOKEN in str(erro.value)


def test_token_vazio_falha():
    with pytest.raises(ErroConfiguracao):
        obter_token({NOME_VARIAVEL_TOKEN: "   "})


def test_token_sem_dois_pontos_falha():
    with pytest.raises(ErroConfiguracao):
        obter_token({NOME_VARIAVEL_TOKEN: "123456"})


def test_token_valido_e_devolvido_sem_espacos():
    assert obter_token({NOME_VARIAVEL_TOKEN: " 123456:ABC-def "}) == "123456:ABC-def"


def test_token_nunca_aparece_na_mensagem_de_erro():
    segredo = "987654:SEGREDO-QUE-NAO-PODE-VAZAR"
    with pytest.raises(ErroConfiguracao) as erro:
        obter_token({NOME_VARIAVEL_TOKEN: segredo + ":"})
    assert segredo not in str(erro.value)
