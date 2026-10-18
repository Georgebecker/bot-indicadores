"""Handlers dos comandos do bot.

As mensagens são curtas (limite do Telegram), em texto simples e em português.
Nenhuma exceção bruta chega ao chat: falha da API vira mensagem amigável.
"""

from __future__ import annotations

import logging

from .bcb import CODIGOS, ClienteSGS, ErroBCB
from .formatacao import acumulado_percentual, data_br, mes_ano, moeda, percentual

logger = logging.getLogger(__name__)

MENSAGEM_BOAS_VINDAS = (
    "Olá! Eu consulto indicadores econômicos do Banco Central do Brasil.\n\n"
    "Comandos disponíveis:\n"
    "/dolar — cotação PTAX de venda do dólar\n"
    "/selic — taxa Selic meta\n"
    "/ipca — IPCA acumulado em 12 meses\n"
    "/poupanca — rendimento da poupança\n\n"
    "Os dados vêm da API SGS do BCB, com a data de referência de cada valor."
)

MENSAGEM_ERRO = (
    "Não consegui falar com o Banco Central agora. "
    "A API pode estar fora do ar ou lenta — tente de novo em alguns minutos."
)

ROTULO = {
    "dolar": "Dólar PTAX (venda)",
    "selic": "Selic meta",
    "ipca": "IPCA",
    "poupanca": "Poupança",
}


class ComandosIndicadores:
    """Handlers agrupados; recebem o cliente do BCB por injeção (facilita teste)."""

    def __init__(self, cliente: ClienteSGS) -> None:
        self._cliente = cliente

    async def start(self, update, context) -> None:
        await update.message.reply_text(MENSAGEM_BOAS_VINDAS)

    async def dolar(self, update, context) -> None:
        await self._responder(update, "dolar")

    async def selic(self, update, context) -> None:
        await self._responder(update, "selic")

    async def ipca(self, update, context) -> None:
        await self._responder(update, "ipca")

    async def poupanca(self, update, context) -> None:
        await self._responder(update, "poupanca")

    async def _responder(self, update, indicador: str) -> None:
        try:
            texto = await self._montar_texto(indicador)
        except ErroBCB as erro:
            logger.warning("falha ao consultar %s: %s", indicador, erro)
            await update.message.reply_text(MENSAGEM_ERRO)
            return
        await update.message.reply_text(texto)

    async def _montar_texto(self, indicador: str) -> str:
        codigo = CODIGOS[indicador]
        if indicador == "ipca":
            return await self._texto_ipca(codigo)
        pontos = await self._cliente.ultimos(codigo, 1)
        ultimo = pontos[-1]
        if indicador == "dolar":
            valor = moeda(ultimo.valor)
        else:
            valor = percentual(ultimo.valor, casas=2) + (
                " ao mês" if indicador == "poupanca" else " ao ano"
            )
        return (
            f"{ROTULO[indicador]}: {valor}\n"
            f"Referência: {data_br(ultimo.data)}\n"
            f"Fonte: Banco Central (SGS {codigo})"
        )

    async def _texto_ipca(self, codigo: int) -> str:
        pontos = await self._cliente.ultimos(codigo, 12)
        acumulado = acumulado_percentual([ponto.valor for ponto in pontos])
        ultimo = pontos[-1]
        return (
            f"{ROTULO['ipca']}: {percentual(acumulado)} em 12 meses\n"
            f"Último mês ({mes_ano(ultimo.data)}): {percentual(ultimo.valor)}\n"
            f"Fonte: Banco Central (SGS {codigo})"
        )
