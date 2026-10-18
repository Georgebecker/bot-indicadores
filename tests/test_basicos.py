"""Testes das peças básicas: leitura do token e números em português.

Duas ideias para guardar deste arquivo:

1. Um erro de configuração precisa **explicar o que fazer** — e nunca mostrar o valor
   do token, senão ele vaza para a tela, para o log e para o print.
2. No Brasil o decimal é vírgula. "5.2079" seria lido como cinco mil duzentos e sete;
   por isso a conversão tem teste, é detalhe pequeno que estraga a leitura inteira.
"""

from __future__ import annotations

from datetime import date

import pytest

from bot_indicadores.config import ErroConfiguracao, NOME_VARIAVEL_TOKEN, obter_token
from bot_indicadores.formatacao import (
    acumulado_percentual,
    data_br,
    mes_ano,
    moeda,
    percentual,
)


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Datas e números
# ---------------------------------------------------------------------------

def test_data_br():
    """Data no formato brasileiro: dia/mês/ano."""
    assert data_br(date(2026, 10, 1)) == "01/10/2026"


def test_mes_ano():
    """Mês e ano, para falar do "último mês" do IPCA."""
    assert mes_ano(date(2026, 9, 1)) == "09/2026"


def test_moeda_usa_virgula_decimal():
    """Reais com vírgula decimal e ponto de milhar."""
    assert moeda(5.2079) == "R$ 5,2079"
    assert moeda(1234.5, casas=2) == "R$ 1.234,50"


def test_percentual_usa_virgula_decimal():
    """Percentual também usa vírgula (e aceita valor negativo)."""
    assert percentual(13.75) == "13,75%"
    assert percentual(-0.5) == "-0,50%"


def test_acumulado_compõe_doze_meses():
    """Acumular é multiplicar, não somar.

    Doze meses de 0,44% dão 5,41% (e não 5,28%, que seria a soma ingênua).
    """
    assert acumulado_percentual([0.44] * 12) == 5.41
    assert acumulado_percentual([0.0] * 12) == 0.0
