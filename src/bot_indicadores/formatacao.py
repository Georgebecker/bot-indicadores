"""Formatação de números e datas no jeito brasileiro.

Problema que este arquivo resolve: o Python escreve números no jeito americano
(`5.2079`), mas no Brasil usamos vírgula (`5,2079`). E não queremos depender de
configuração de idioma do computador, porque isso muda de máquina para máquina.

Então escrevemos as regras à mão, de forma simples e previsível:

    5.2079      -> "5,2079"
    1234.5      -> "1.234,50"
    13.75       -> "13,75%"
"""

from __future__ import annotations

from datetime import date


def _com_virgula(texto: str) -> str:
    """Troca os separadores do padrão americano para o brasileiro.

    O truque: primeiro trocamos a vírgula por um símbolo temporário (\\x00),
    depois trocamos o ponto por vírgula, e por fim devolvemos o símbolo como ponto.
    Sem esse passo do meio, "1,234.5" viraria uma bagunça.

    Exemplo: "1,234.50" -> "1.234,50"
    """
    return texto.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def data_br(dia: date) -> str:
    """Mostra a data como 01/10/2026 (dia/mês/ano)."""
    return dia.strftime("%d/%m/%Y")


def mes_ano(dia: date) -> str:
    """Mostra só mês e ano, como 09/2026 — útil para falar do 'último mês'."""
    return dia.strftime("%m/%Y")


def moeda(valor: float, casas: int = 4) -> str:
    """Mostra um valor em reais, com vírgula decimal.

    O dólar PTAX é divulgado com quatro casas decimais, por isso o padrão 4.
    """
    # f"{valor:,.4f}" produz "5.2079" ou "1,234.5678" (padrão americano).
    return "R$ " + _com_virgula(f"{valor:,.{casas}f}")


def percentual(valor: float, casas: int = 2) -> str:
    """Mostra um percentual com vírgula: 13.75 -> "13,75%"."""
    return _com_virgula(f"{valor:,.{casas}f}") + "%"


def acumulado_percentual(valores_mensais: list[float], casas: int = 2) -> float:
    """Junta várias taxas mensais em uma taxa acumulada.

    Cuidado que muita gente erra: não é soma, é **multiplicação**.
    Imagine que um produto custa 100 e sobe 10%: vai para 110. Se no mês seguinte
    subir 10% de novo, sobe sobre 110, não sobre 100 — vai para 121, e não 120.
    Por isso somar 10 + 10 = 20% daria errado; o certo é 21%.

    Cada valor mensal é dividido por 100, somado a 1 (virando um "fator" de
    multiplicação) e multiplicado pelos anteriores. No fim, desfazemos a conta.

    Exemplo: doze meses de 0,44% -> 5,41% acumulados (e não 5,28%).
    """
    # Começamos com 1.0 porque 1 é o "neutro" da multiplicação:
    # qualquer número multiplicado por 1 continua igual.
    fator = 1.0
    for valor in valores_mensais:
        fator *= 1 + valor / 100
    # (fator - 1) * 100 devolve o resultado em porcentagem, arredondado.
    return round((fator - 1) * 100, casas)
