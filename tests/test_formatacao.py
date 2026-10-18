"""Testes da formatação em português do Brasil.

Aqui a regra é simples e vale a pena memorizar: **no Brasil o decimal é vírgula**.
Um número mostrado como "5.2079" seria lido como cinco mil duzentos e sete no
Brasil. Por isso a conversão precisa de teste — é detalhe pequeno que estraga a
leitura do dado inteiro.
"""

from __future__ import annotations

from datetime import date

from bot_indicadores.formatacao import (
    acumulado_percentual,
    data_br,
    mes_ano,
    moeda,
    percentual,
)


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
