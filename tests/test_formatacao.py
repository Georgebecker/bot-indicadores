"""Testes de formatação em português do Brasil."""

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
    assert data_br(date(2026, 10, 1)) == "01/10/2026"


def test_mes_ano():
    assert mes_ano(date(2026, 9, 1)) == "09/2026"


def test_moeda_usa_virgula_decimal():
    assert moeda(5.2079) == "R$ 5,2079"
    assert moeda(1234.5, casas=2) == "R$ 1.234,50"


def test_percentual_usa_virgula_decimal():
    assert percentual(13.75) == "13,75%"
    assert percentual(-0.5) == "-0,50%"


def test_acumulado_compõe_doze_meses():
    assert acumulado_percentual([0.44] * 12) == 5.41
    assert acumulado_percentual([0.0] * 12) == 0.0
