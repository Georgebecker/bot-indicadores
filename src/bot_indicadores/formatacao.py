"""Formatação de números e datas em português do Brasil, sem depender de locale."""

from __future__ import annotations

from datetime import date


def _com_virgula(texto: str) -> str:
    return texto.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def data_br(dia: date) -> str:
    return dia.strftime("%d/%m/%Y")


def mes_ano(dia: date) -> str:
    return dia.strftime("%m/%Y")


def moeda(valor: float, casas: int = 4) -> str:
    return "R$ " + _com_virgula(f"{valor:,.{casas}f}")


def percentual(valor: float, casas: int = 2) -> str:
    return _com_virgula(f"{valor:,.{casas}f}") + "%"


def acumulado_percentual(valores_mensais: list[float], casas: int = 2) -> float:
    """Acumula variações percentuais mensais por composição."""
    fator = 1.0
    for valor in valores_mensais:
        fator *= 1 + valor / 100
    return round((fator - 1) * 100, casas)
