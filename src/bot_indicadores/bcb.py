"""Cliente assíncrono e somente-leitura da API SGS do Banco Central.

Política de erro (contrato, seção "Classes de Erro"):
- timeout curto e poucas tentativas, para o usuário não ficar esperando;
- resposta que não é JSON (o BCB devolve uma página XML "Requisição inválida!"
  quando bloqueia ou recebe parâmetro errado) é tratada como falha da API;
- `requests` é síncrono, então roda em `asyncio.to_thread` para não travar o
  event loop do python-telegram-bot.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import requests

from .config import URL_SGS_PADRAO

CODIGOS = {"dolar": 1, "selic": 432, "ipca": 433, "poupanca": 195}

CABECALHOS = {
    "Accept": "application/json",
    "User-Agent": "bot-indicadores/1.0 (+https://github.com/Georgebecker/bot-indicadores)",
}

TIMEOUT_PADRAO = 8.0
TENTATIVAS_PADRAO = 2
ESPERA_PADRAO = 1.0
TTL_CACHE_PADRAO = 60.0


class ErroBCB(Exception):
    """Falha ao consultar o BCB: rede, serviço fora, resposta inválida ou sem dados."""


@dataclass(frozen=True)
class Ponto:
    """Um valor de série com a data de referência."""

    data: date
    valor: float


def _converter(bruto: Any) -> list[Ponto]:
    if not isinstance(bruto, list) or not bruto:
        raise ErroBCB("o BCB respondeu sem dados para o período")
    pontos: list[Ponto] = []
    for item in bruto:
        try:
            dia = datetime.strptime(str(item["data"]).strip(), "%d/%m/%Y").date()
            valor = float(str(item["valor"]).strip().replace(",", "."))
        except (KeyError, TypeError, ValueError) as erro:
            raise ErroBCB("o BCB respondeu em formato inesperado") from erro
        pontos.append(Ponto(data=dia, valor=valor))
    return pontos


class ClienteSGS:
    """Consulta os últimos N valores de uma série do SGS."""

    def __init__(
        self,
        sessao: requests.Session | None = None,
        url_base: str = URL_SGS_PADRAO,
        timeout: float = TIMEOUT_PADRAO,
        tentativas: int = TENTATIVAS_PADRAO,
        espera: float = ESPERA_PADRAO,
        ttl_cache: float = TTL_CACHE_PADRAO,
    ) -> None:
        self._sessao = sessao if sessao is not None else requests.Session()
        self._url_base = url_base
        self._timeout = timeout
        self._tentativas = max(1, tentativas)
        self._espera = espera
        self._ttl_cache = ttl_cache
        self._cache: dict[tuple[int, int], tuple[float, list[Ponto]]] = {}

    def limpar_cache(self) -> None:
        self._cache.clear()

    def montar_url(self, codigo: int, quantidade: int) -> str:
        return self._url_base.format(codigo=codigo, quantidade=quantidade)

    async def ultimos(self, codigo: int, quantidade: int = 1) -> list[Ponto]:
        """Devolve os últimos `quantidade` pontos da série, do mais antigo ao mais novo.

        Respostas ficam em cache em memória por `ttl_cache` segundos; nada é gravado
        em disco (o contrato proíbe cache persistente).
        """
        if quantidade < 1:
            raise ValueError("quantidade precisa ser maior que zero")
        chave = (codigo, quantidade)
        agora = time.monotonic()
        guardado = self._cache.get(chave)
        if guardado is not None and agora - guardado[0] < self._ttl_cache:
            return list(guardado[1])
        url = self.montar_url(codigo, quantidade)
        pontos = await asyncio.to_thread(self._baixar, url)
        self._cache[chave] = (time.monotonic(), pontos)
        return list(pontos)

    def _baixar(self, url: str) -> list[Ponto]:
        ultimo_erro: Exception | None = None
        for tentativa in range(1, self._tentativas + 1):
            try:
                return self._tentar_uma_vez(url)
            except (requests.RequestException, ErroBCB) as erro:
                ultimo_erro = erro
                if tentativa < self._tentativas:
                    time.sleep(self._espera)
        if isinstance(ultimo_erro, ErroBCB):
            raise ultimo_erro
        raise ErroBCB("não foi possível falar com a API do BCB") from ultimo_erro

    def _tentar_uma_vez(self, url: str) -> list[Ponto]:
        resposta = self._sessao.get(url, timeout=self._timeout, headers=CABECALHOS)
        if resposta.status_code >= 500:
            raise ErroBCB(f"o BCB respondeu com erro {resposta.status_code}")
        resposta.raise_for_status()
        try:
            dados = resposta.json()
        except ValueError as erro:
            raise ErroBCB("o BCB respondeu em formato inesperado") from erro
        if isinstance(dados, dict) and "erro" in dados:
            raise ErroBCB("o BCB reportou erro interno na consulta")
        return _converter(dados)
