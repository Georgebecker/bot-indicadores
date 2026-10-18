"""O que o bot responde para cada comando.

Pense neste arquivo como o **atendente** do bot. Quando alguém escreve /dolar,
o Telegram avisa o bot, e o atendente decide: qual número buscar, como escrever a
resposta e o que dizer se o Banco Central não responder.

Regra de ouro da conversa: mensagens curtas (o Telegram tem limite de tamanho),
texto simples (sem tabela) e nenhum erro técnico aparecendo para o usuário.
"""

from __future__ import annotations

import logging

from .bcb import CODIGOS, ClienteSGS, ErroBCB
from .formatacao import acumulado_percentual, data_br, mes_ano, moeda, percentual

# "logging" é o caderno de anotações do programa: guarda o que aconteceu, para
# podermos investigar depois sem mostrar nada disso para quem usa o bot.
logger = logging.getLogger(__name__)

# A primeira mensagem: quem chega precisa saber o que pode pedir.
MENSAGEM_BOAS_VINDAS = (
    "Olá! Eu consulto indicadores econômicos do Banco Central do Brasil.\n\n"
    "Comandos disponíveis:\n"
    "/dolar — cotação PTAX de venda do dólar\n"
    "/selic — taxa Selic meta\n"
    "/ipca — IPCA acumulado em 12 meses\n"
    "/poupanca — rendimento da poupança\n\n"
    "Os dados vêm da API SGS do BCB, com a data de referência de cada valor."
)

# A mensagem quando algo dá errado do lado de fora.
# Repare no que ela NÃO tem: nome de erro, código HTTP, "traceback". O usuário
# não precisa disso e, muitas vezes, não entenderia. Ele precisa saber o que fazer.
MENSAGEM_ERRO = (
    "Não consegui falar com o Banco Central agora. "
    "A API pode estar fora do ar ou lenta — tente de novo em alguns minutos."
)

# Nome bonito de cada indicador, para aparecer na resposta.
ROTULO = {
    "dolar": "Dólar PTAX (venda)",
    "selic": "Selic meta",
    "ipca": "IPCA",
    "poupanca": "Poupança",
}


class ComandosIndicadores:
    """Guarda as respostas de cada comando.

    O cliente do Banco Central entra pelo construtor ("injeção de dependência"):
    assim conseguimos testar o atendente com um cliente de mentira, sem internet.
    """

    def __init__(self, cliente: ClienteSGS) -> None:
        self._cliente = cliente

    async def start(self, update, context) -> None:
        """Responde ao /start com a lista de comandos."""
        # `update` é a mensagem que chegou; `message.reply_text` envia a resposta.
        await update.message.reply_text(MENSAGEM_BOAS_VINDAS)

    async def dolar(self, update, context) -> None:
        """Responde ao /dolar."""
        await self._responder(update, "dolar")

    async def selic(self, update, context) -> None:
        """Responde ao /selic."""
        await self._responder(update, "selic")

    async def ipca(self, update, context) -> None:
        """Responde ao /ipca."""
        await self._responder(update, "ipca")

    async def poupanca(self, update, context) -> None:
        """Responde ao /poupanca."""
        await self._responder(update, "poupanca")

    async def _responder(self, update, indicador: str) -> None:
        """Caminho comum dos comandos: tenta montar o texto e trata a falha.

        Estar tudo aqui (em vez de repetido em cada comando) significa que, se um
        dia a mensagem de erro mudar, ela muda em um lugar só.
        """
        try:
            texto = await self._montar_texto(indicador)
        except ErroBCB as erro:
            # Anotamos o detalhe técnico no caderno (log), mas não no chat.
            logger.warning("falha ao consultar %s: %s", indicador, erro)
            await update.message.reply_text(MENSAGEM_ERRO)
            return
        await update.message.reply_text(texto)

    async def _montar_texto(self, indicador: str) -> str:
        """Monta a mensagem final de um indicador (sem enviar nada)."""
        codigo = CODIGOS[indicador]

        # O IPCA é o único que precisa de 12 valores, porque queremos o acumulado
        # dos últimos doze meses. Os outros bastam com o último valor.
        if indicador == "ipca":
            return await self._texto_ipca(codigo)

        pontos = await self._cliente.ultimos(codigo, 1)
        ultimo = pontos[-1]  # a lista vem do mais antigo para o mais novo

        if indicador == "dolar":
            # Dólar é dinheiro: mostramos com "R$" e quatro casas.
            valor = moeda(ultimo.valor)
        else:
            # Selic é ao ano; poupança é ao mês. São coisas diferentes!
            valor = percentual(ultimo.valor, casas=2) + (
                " ao mês" if indicador == "poupanca" else " ao ano"
            )

        # Sempre mostramos a data: um número sem data pode ser de hoje ou de
        # três meses atrás, e isso muda completamente a leitura.
        return (
            f"{ROTULO[indicador]}: {valor}\n"
            f"Referência: {data_br(ultimo.data)}\n"
            f"Fonte: Banco Central (SGS {codigo})"
        )

    async def _texto_ipca(self, codigo: int) -> str:
        """Monta a mensagem do IPCA: acumulado de 12 meses + último mês."""
        pontos = await self._cliente.ultimos(codigo, 12)

        # Pegamos só a lista de valores e deixamos a conta com `acumulado_percentual`.
        acumulado = acumulado_percentual([ponto.valor for ponto in pontos])
        ultimo = pontos[-1]

        return (
            f"{ROTULO['ipca']}: {percentual(acumulado)} em 12 meses\n"
            f"Último mês ({mes_ano(ultimo.data)}): {percentual(ultimo.valor)}\n"
            f"Fonte: Banco Central (SGS {codigo})"
        )
