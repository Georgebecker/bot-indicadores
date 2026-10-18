"""Testes do cliente da API SGS — nenhuma chamada de rede real."""

from __future__ import annotations

import pytest
import requests

from bot_indicadores.bcb import CODIGOS, ClienteSGS, ErroBCB, Ponto


class RespostaFalsa:
    def __init__(self, corpo, status=200, json_valido=True):
        self._corpo = corpo
        self.status_code = status
        self._json_valido = json_valido

    def json(self):
        if not self._json_valido:
            raise ValueError("não é JSON")
        return self._corpo

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")


class SessaoFalsa:
    def __init__(self, respostas):
        self._respostas = list(respostas)
        self.chamadas: list[str] = []

    def get(self, url, timeout=None, headers=None):
        self.chamadas.append(url)
        resposta = self._respostas.pop(0)
        if isinstance(resposta, Exception):
            raise resposta
        return resposta


def cliente(sessao, tentativas=2):
    return ClienteSGS(sessao=sessao, tentativas=tentativas, espera=0)


def test_codigos_do_contrato():
    assert CODIGOS == {"dolar": 1, "selic": 432, "ipca": 433, "poupanca": 195}


def test_montar_url_usa_codigo_e_quantidade():
    url = cliente(SessaoFalsa([])).montar_url(433, 12)
    assert url.endswith("/bcdata.sgs.433/dados/ultimos/12")


async def test_ultimos_converte_data_e_valor():
    sessao = SessaoFalsa([RespostaFalsa([{"data": "01/10/2026", "valor": "5.2079"}])])
    pontos = await cliente(sessao).ultimos(1, 1)
    assert pontos == [Ponto(data=pontos[0].data, valor=5.2079)]
    assert pontos[0].data.isoformat() == "2026-10-01"


async def test_erro_500_vira_erro_bcb():
    sessao = SessaoFalsa([RespostaFalsa({}, status=500), RespostaFalsa({}, status=500)])
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(432, 1)
    assert len(sessao.chamadas) == 2


async def test_resposta_html_vira_erro_bcb():
    sessao = SessaoFalsa([RespostaFalsa("<html>Requisição inválida!</html>", json_valido=False)] * 2)
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(432, 1)


async def test_erro_json_do_bcb_vira_erro_bcb():
    sessao = SessaoFalsa([RespostaFalsa({"erro": {"statusCode": 500}})] * 2)
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(432, 1)


async def test_lista_vazia_vira_erro_bcb():
    sessao = SessaoFalsa([RespostaFalsa([])] * 2)
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(1, 1)


async def test_item_malformado_vira_erro_bcb():
    sessao = SessaoFalsa([RespostaFalsa([{"data": "ontem", "valor": "abc"}])] * 2)
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(1, 1)


async def test_tenta_de_novo_e_devolve_no_segundo_sucesso():
    sessao = SessaoFalsa(
        [
            requests.ConnectionError("caiu"),
            RespostaFalsa([{"data": "01/10/2026", "valor": "0.44"}]),
        ]
    )
    pontos = await cliente(sessao).ultimos(433, 1)
    assert pontos[-1].valor == 0.44
    assert len(sessao.chamadas) == 2


async def test_quantidade_invalida():
    with pytest.raises(ValueError):
        await cliente(SessaoFalsa([])).ultimos(1, 0)


async def test_cache_evita_segunda_chamada_http():
    sessao = SessaoFalsa([RespostaFalsa([{"data": "01/10/2026", "valor": "5.2"}])])
    cliente_com_cache = cliente(sessao)
    await cliente_com_cache.ultimos(1, 1)
    await cliente_com_cache.ultimos(1, 1)
    assert len(sessao.chamadas) == 1


async def test_cache_separa_series_diferentes():
    sessao = SessaoFalsa(
        [
            RespostaFalsa([{"data": "01/10/2026", "valor": "5.2"}]),
            RespostaFalsa([{"data": "01/10/2026", "valor": "13.75"}]),
        ]
    )
    cliente_com_cache = cliente(sessao)
    assert (await cliente_com_cache.ultimos(1, 1))[0].valor == 5.2
    assert (await cliente_com_cache.ultimos(432, 1))[0].valor == 13.75
    assert len(sessao.chamadas) == 2


async def test_cache_expira_com_ttl_zero():
    sessao = SessaoFalsa(
        [
            RespostaFalsa([{"data": "01/10/2026", "valor": "5.2"}]),
            RespostaFalsa([{"data": "02/10/2026", "valor": "5.3"}]),
        ]
    )
    sem_cache = ClienteSGS(sessao=sessao, tentativas=1, espera=0, ttl_cache=0)
    await sem_cache.ultimos(1, 1)
    await sem_cache.ultimos(1, 1)
    assert len(sessao.chamadas) == 2
