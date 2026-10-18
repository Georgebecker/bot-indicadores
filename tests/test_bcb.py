"""Testes do cliente do Banco Central — sem usar a internet.

Por que existe um arquivo de testes? Porque ler o código e "achar que está certo"
não prova nada. Um teste é uma frase que o computador verifica sozinho, toda vez.

Aqui existe um truque importante: em vez de conversar com o Banco Central de
verdade (que pode estar fora do ar, como já aconteceu), usamos **dublês** —
objetos que fingem ser a internet e devolvem exatamente a resposta que queremos
testar. É como ensaiar uma peça com um ator substituto: dá para testar a cena de
chuva sem depender do tempo.
"""

from __future__ import annotations

import pytest
import requests

from bot_indicadores.bcb import CODIGOS, ClienteSGS, ErroBCB, Ponto


class RespostaFalsa:
    """Finge ser a resposta de um site.

    Um site de verdade devolve: um código de status (200 = ok, 500 = erro do
    servidor), um corpo (o texto) e a capacidade de "virar" JSON.
    """

    def __init__(self, corpo, status=200, json_valido=True):
        self._corpo = corpo
        self.status_code = status
        self._json_valido = json_valido

    def json(self):
        """Devolve o corpo como dado. Se pedirmos para simular HTML, dá erro."""
        if not self._json_valido:
            raise ValueError("não é JSON")
        return self._corpo

    def raise_for_status(self):
        """Imita o comportamento do requests para código de erro (400 ou mais)."""
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")


class SessaoFalsa:
    """Finge ser a conexão com a internet.

    Recebe uma fila de respostas. Cada chamada `get` entrega a próxima da fila e
    anota o endereço pedido — assim conseguimos conferir quantas chamadas houve.
    """

    def __init__(self, respostas):
        self._respostas = list(respostas)
        self.chamadas: list[str] = []

    def get(self, url, timeout=None, headers=None):
        self.chamadas.append(url)
        resposta = self._respostas.pop(0)  # tira a primeira resposta da fila
        if isinstance(resposta, Exception):
            raise resposta  # simula falha de rede
        return resposta


def cliente(sessao, tentativas=2):
    """Cria um cliente com os dublês e sem espera real entre tentativas."""
    # `espera=0` deixa o teste rápido; `tentativas=2` é o comportamento real.
    return ClienteSGS(sessao=sessao, tentativas=tentativas, espera=0)


# ---------------------------------------------------------------------------
# Os números das séries estão corretos?
# ---------------------------------------------------------------------------

def test_codigos_do_contrato():
    """O contrato manda usar estas quatro séries — e só estas."""
    assert CODIGOS == {"dolar": 1, "selic": 432, "ipca": 433, "poupanca": 195}


def test_montar_url_usa_codigo_e_quantidade():
    """O endereço precisa levar o código da série e quantos valores queremos."""
    url = cliente(SessaoFalsa([])).montar_url(433, 12)
    assert url.endswith("/bcdata.sgs.433/dados/ultimos/12")


# ---------------------------------------------------------------------------
# Resposta boa: o que o cliente devolve?
# ---------------------------------------------------------------------------

async def test_ultimos_converte_data_e_valor():
    """Texto do BCB vira data e número de verdade.

    O BCB manda "01/10/2026" e "5.2079" como texto. Depois do cliente, isso
    precisa ser uma data e um número — senão não conseguimos formatar nada.
    """
    sessao = SessaoFalsa([RespostaFalsa([{"data": "01/10/2026", "valor": "5.2079"}])])
    pontos = await cliente(sessao).ultimos(1, 1)
    assert pontos == [Ponto(data=pontos[0].data, valor=5.2079)]
    assert pontos[0].data.isoformat() == "2026-10-01"


# ---------------------------------------------------------------------------
# Resposta ruim: cada tipo de problema vira um erro tratável
# ---------------------------------------------------------------------------

async def test_erro_500_vira_erro_bcb():
    """Servidor fora do ar (500) vira ErroBCB — e tentamos duas vezes."""
    sessao = SessaoFalsa([RespostaFalsa({}, status=500), RespostaFalsa({}, status=500)])
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(432, 1)
    assert len(sessao.chamadas) == 2


async def test_resposta_html_vira_erro_bcb():
    """Às vezes o BCB devolve uma página HTML em vez de JSON.

    Isso acontece quando ele bloqueia o acesso ou recebe parâmetro errado.
    HTML não é JSON, então o cliente precisa tratar como falha (e não travar).
    """
    sessao = SessaoFalsa(
        [RespostaFalsa("<html>Requisição inválida!</html>", json_valido=False)] * 2
    )
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(432, 1)


async def test_erro_json_do_bcb_vira_erro_bcb():
    """Às vezes vem HTTP 200 com um aviso de erro dentro do JSON.

    "200" normalmente significa "deu certo", mas o colégio do BCB às vezes
    responde com um erro no corpo. Não podemos confiar só no código HTTP.
    """
    sessao = SessaoFalsa([RespostaFalsa({"erro": {"statusCode": 500}})] * 2)
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(432, 1)


async def test_lista_vazia_vira_erro_bcb():
    """Lista vazia = não há dado (fim de semana, feriado, período sem registro)."""
    sessao = SessaoFalsa([RespostaFalsa([])] * 2)
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(1, 1)


async def test_item_malformado_vira_erro_bcb():
    """Se algum item vier estranho, é melhor falhar do que mostrar número errado."""
    sessao = SessaoFalsa([RespostaFalsa([{"data": "ontem", "valor": "abc"}])] * 2)
    with pytest.raises(ErroBCB):
        await cliente(sessao).ultimos(1, 1)


# ---------------------------------------------------------------------------
# Tentativas: insistir uma vez costuma resolver oscilação de rede
# ---------------------------------------------------------------------------

async def test_tenta_de_novo_e_devolve_no_segundo_sucesso():
    """Primeira tentativa cai, segunda funciona: o usuário recebe o resultado."""
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
    """Pedir "zero valores" é um pedido sem sentido: avisamos na hora."""
    with pytest.raises(ValueError):
        await cliente(SessaoFalsa([])).ultimos(1, 0)


# ---------------------------------------------------------------------------
# Memória curta (cache)
# ---------------------------------------------------------------------------

async def test_cache_evita_segunda_chamada_http():
    """Duas consultas iguais em menos de 60 s = só uma ida ao Banco Central."""
    sessao = SessaoFalsa([RespostaFalsa([{"data": "01/10/2026", "valor": "5.2"}])])
    cliente_com_cache = cliente(sessao)
    await cliente_com_cache.ultimos(1, 1)
    await cliente_com_cache.ultimos(1, 1)
    assert len(sessao.chamadas) == 1


async def test_cache_separa_series_diferentes():
    """Dólar e Selic são coisas diferentes: um não pode "contaminar" o outro."""
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
    """Com validade zero, toda consulta volta a perguntar (o cache não "gruda")."""
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
