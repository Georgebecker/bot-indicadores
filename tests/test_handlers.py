"""Testes dos handlers: mensagens, acumulado do IPCA e falha amigável."""

from __future__ import annotations

from datetime import date

from bot_indicadores.bcb import ErroBCB, Ponto
from bot_indicadores.handlers import (
    MENSAGEM_BOAS_VINDAS,
    MENSAGEM_ERRO,
    ComandosIndicadores,
)


class MensagemFalsa:
    def __init__(self):
        self.respostas: list[str] = []

    async def reply_text(self, texto):
        self.respostas.append(texto)


class UpdateFalso:
    def __init__(self):
        self.message = MensagemFalsa()


class ClienteFalso:
    def __init__(self, pontos_por_codigo=None, erro=False):
        self._pontos = pontos_por_codigo or {}
        self._erro = erro
        self.pedidos: list[tuple[int, int]] = []

    async def ultimos(self, codigo, quantidade=1):
        self.pedidos.append((codigo, quantidade))
        if self._erro:
            raise ErroBCB("API fora do ar")
        return self._pontos[codigo]


def cliente_padrao():
    return ClienteFalso(
        {
            1: [Ponto(date(2026, 10, 1), 5.2079)],
            432: [Ponto(date(2026, 10, 1), 13.75)],
            433: [Ponto(date(2025, 11, 1), 0.44)] * 11
            + [Ponto(date(2026, 9, 1), 0.44)],
            195: [Ponto(date(2026, 10, 1), 0.50)],
        }
    )


async def test_start_lista_os_quatro_comandos():
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).start(update, None)
    texto = update.message.respostas[0]
    assert texto == MENSAGEM_BOAS_VINDAS
    for comando in ("/dolar", "/selic", "/ipca", "/poupanca"):
        assert comando in texto


async def test_dolar_mostra_valor_e_data_de_referencia():
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).dolar(update, None)
    texto = update.message.respostas[0]
    assert "R$ 5,2079" in texto
    assert "01/10/2026" in texto
    assert "SGS 1" in texto


async def test_selic_mostra_percentual_ao_ano():
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).selic(update, None)
    texto = update.message.respostas[0]
    assert "13,75% ao ano" in texto
    assert "SGS 432" in texto


async def test_ipca_acumula_doze_meses():
    cliente = cliente_padrao()
    update = UpdateFalso()
    await ComandosIndicadores(cliente).ipca(update, None)
    texto = update.message.respostas[0]
    assert "5,41% em 12 meses" in texto
    assert "Último mês (09/2026): 0,44%" in texto
    assert cliente.pedidos == [(433, 12)]


async def test_poupanca_mostra_percentual_ao_mes():
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).poupanca(update, None)
    texto = update.message.respostas[0]
    assert "0,50% ao mês" in texto
    assert "SGS 195" in texto
    assert "01/10/2026" in texto


async def test_falha_da_api_responde_mensagem_amigavel():
    update = UpdateFalso()
    await ComandosIndicadores(ClienteFalso(erro=True)).dolar(update, None)
    assert update.message.respostas == [MENSAGEM_ERRO]
    assert "Traceback" not in update.message.respostas[0]
    assert "ErroBCB" not in update.message.respostas[0]


async def test_falha_da_api_nao_vaza_excecao_no_chat_em_nenhum_comando():
    for nome in ("dolar", "selic", "ipca", "poupanca"):
        update = UpdateFalso()
        comandos = ComandosIndicadores(ClienteFalso(erro=True))
        await getattr(comandos, nome)(update, None)
        assert update.message.respostas == [MENSAGEM_ERRO], nome
