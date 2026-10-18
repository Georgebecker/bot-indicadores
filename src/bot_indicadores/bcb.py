"""Cliente da API SGS do Banco Central — quem realmente busca os números.

Imagine que o Banco Central tem um balcão de atendimento. Você pede "quero os dois
últimos valores da série 432" e ele te entrega uma lista. Este arquivo é o nosso
mensageiro: monta o pedido, vai até o balcão, espera a resposta e traduz o que
voltou para algo que o bot entende.

Três cuidados importantes que estão implementados aqui:

1. **Não travar o bot.** A conversa com o banco é lenta (pode levar segundos).
   Se esperássemos parados, o bot ficaria "travado" para todos os outros usuários.
   Por isso usamos `asyncio.to_thread`: a espera acontece em outra "linha de
   atendimento", enquanto o bot continua respondendo.

2. **Falhar com educação.** Rede cai, servidor fica fora do ar, o BCB bloqueia
   acessos em excesso. O usuário final nunca deve ver um erro técnico — ele recebe
   uma frase simples explicando que não deu e que pode tentar depois.

3. **Não repetir trabalho.** Se duas pessoas pedirem o mesmo indicador em menos de
   60 segundos, a segunda recebe a mesma resposta guardada, sem incomodar o BCB.
   Isso se chama *cache* (uma "memória curta").
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import requests

from .config import URL_SGS_PADRAO

# Números que identificam cada série no Banco Central.
# SGS é o sistema onde o BCB publica essas séries históricas.
CODIGOS = {
    "dolar": 1,  # Dólar PTAX (venda)
    "selic": 432,  # Taxa Selic meta
    "ipca": 433,  # IPCA mensal
    "poupanca": 195,  # Rendimento da poupança
}

# O que avisamos ao servidor sobre quem somos e o que aceitamos receber.
# Pedir "application/json" é como dizer: "responda em JSON, por favor".
CABECALHOS = {
    "Accept": "application/json",
    "User-Agent": "bot-indicadores/1.0 (+https://github.com/Georgebecker/bot-indicadores)",
}

# Quanto tempo esperamos por resposta, quantas vezes tentamos e quanto esperamos
# entre uma tentativa e outra. Valores curtos de propósito: ninguém gosta de
# esperar 30 segundos por uma mensagem no Telegram.
TIMEOUT_PADRAO = 8.0
TENTATIVAS_PADRAO = 2
ESPERA_PADRAO = 1.0

# Quanto tempo uma resposta fica guardada na memória curta (em segundos).
TTL_CACHE_PADRAO = 60.0


class ErroBCB(Exception):
    """Algo deu errado na conversa com o Banco Central.

    Usamos um erro só para todos os casos (rede, servidor fora, resposta estranha,
    sem dados) porque, para quem está no Telegram, o resultado é o mesmo: uma
    mensagem amigável e a chance de tentar de novo.
    """


@dataclass(frozen=True)
class Ponto:
    """Um único valor de uma série, com a data a que ele se refere.

    `frozen=True` significa "não pode ser alterado depois de criado" — é como uma
    foto tirada do valor: ninguém sai riscando o número.
    """

    data: date
    valor: float


def _converter(bruto: Any) -> list[Ponto]:
    """Transforma a resposta crua do BCB em uma lista de `Ponto`.

    O BCB responde algo assim:
        [{"data": "01/10/2026", "valor": "5.2079"}]
    Repare que a data vem como texto no formato dia/mês/ano e o valor também vem
    como texto. Aqui convertemos os dois para tipos de verdade (data e número).
    """
    # Se não veio uma lista, ou veio uma lista vazia, não há dado para usar.
    if not isinstance(bruto, list) or not bruto:
        raise ErroBCB("o BCB respondeu sem dados para o período")

    pontos: list[Ponto] = []
    for item in bruto:
        try:
            # strptime lê texto com formato; strftime escreve. "%d/%m/%Y" é dia/mês/ano.
            dia = datetime.strptime(str(item["data"]).strip(), "%d/%m/%Y").date()
            # Alguns servidores usam vírgula decimal; trocamos por ponto antes de converter.
            valor = float(str(item["valor"]).strip().replace(",", "."))
        except (KeyError, TypeError, ValueError) as erro:
            # Se qualquer item vier estranho, tratamos o pacote inteiro como falha.
            raise ErroBCB("o BCB respondeu em formato inesperado") from erro
        pontos.append(Ponto(data=dia, valor=valor))
    return pontos


class ClienteSGS:
    """Busca os últimos valores de uma série do Banco Central."""

    def __init__(
        self,
        sessao: requests.Session | None = None,
        url_base: str = URL_SGS_PADRAO,
        timeout: float = TIMEOUT_PADRAO,
        tentativas: int = TENTATIVAS_PADRAO,
        espera: float = ESPERA_PADRAO,
        ttl_cache: float = TTL_CACHE_PADRAO,
    ) -> None:
        # `sessao` é o objeto que realmente faz as chamadas HTTP.
        # Receber de fora permite trocar por um "dublê" nos testes, sem internet.
        self._sessao = sessao if sessao is not None else requests.Session()
        self._url_base = url_base
        self._timeout = timeout
        # `max(1, ...)` garante pelo menos uma tentativa, mesmo se alguém passar 0.
        self._tentativas = max(1, tentativas)
        self._espera = espera
        self._ttl_cache = ttl_cache
        # A memória curta: para cada código de série, guardamos
        # (momento em que foi buscado, lista de pontos).
        self._cache: dict[tuple[int, int], tuple[float, list[Ponto]]] = {}

    def limpar_cache(self) -> None:
        """Esquece tudo que estava guardado (útil em teste e para forçar dado novo)."""
        self._cache.clear()

    def montar_url(self, codigo: int, quantidade: int) -> str:
        """Monta o endereço da consulta preenchendo os espaços `{}` do modelo."""
        return self._url_base.format(codigo=codigo, quantidade=quantidade)

    async def ultimos(self, codigo: int, quantidade: int = 1) -> list[Ponto]:
        """Devolve os últimos `quantidade` valores da série.

        A lista volta do mais antigo para o mais novo, então o último item é o
        valor mais recente — é ele que normalmente mostramos ao usuário.
        """
        if quantidade < 1:
            raise ValueError("quantidade precisa ser maior que zero")

        chave = (codigo, quantidade)

        # `time.monotonic` é um relógio que só anda para frente — bom para medir
        # quanto tempo passou, sem se confundir com ajustes de horário do sistema.
        agora = time.monotonic()
        guardado = self._cache.get(chave)
        if guardado is not None and agora - guardado[0] < self._ttl_cache:
            # Ainda está "quente": devolvemos a cópia guardada, sem chamar a internet.
            # `list(...)` cria uma cópia para quem receber não alterar o cache sem querer.
            return list(guardado[1])

        url = self.montar_url(codigo, quantidade)

        # Aqui está o cuidado número 1: a função `_baixar` é síncrona (bloqueante).
        # `to_thread` a coloca em uma linha de execução separada, então o bot não trava.
        pontos = await asyncio.to_thread(self._baixar, url)

        # Guardamos o resultado para os próximos 60 segundos.
        self._cache[chave] = (time.monotonic(), pontos)
        return list(pontos)

    def _baixar(self, url: str) -> list[Ponto]:
        """Tenta buscar a URL algumas vezes antes de desistir.

        Tentar de novo ajuda quando a falha é passageira (uma oscilação de rede,
        por exemplo). Mas não tentamos para sempre: duas tentativas é o combinado.
        """
        ultimo_erro: Exception | None = None
        for tentativa in range(1, self._tentativas + 1):
            try:
                return self._tentar_uma_vez(url)
            except (requests.RequestException, ErroBCB) as erro:
                ultimo_erro = erro
                # Só esperamos se ainda houver outra tentativa pela frente.
                if tentativa < self._tentativas:
                    time.sleep(self._espera)

        # Se já era um erro nosso (ErroBCB), repassamos como está.
        if isinstance(ultimo_erro, ErroBCB):
            raise ultimo_erro
        # Se era falha de rede, embrulhamos em nossa mensagem amigável.
        raise ErroBCB("não foi possível falar com a API do BCB") from ultimo_erro

    def _tentar_uma_vez(self, url: str) -> list[Ponto]:
        """Faz uma única chamada e confere se a resposta faz sentido."""
        resposta = self._sessao.get(url, timeout=self._timeout, headers=CABECALHOS)

        # 5xx significa "o problema é do servidor deles", não do nosso pedido.
        if resposta.status_code >= 500:
            raise ErroBCB(f"o BCB respondeu com erro {resposta.status_code}")

        # 4xx significa "o pedido está errado": levanta erro do próprio requests.
        resposta.raise_for_status()

        try:
            dados = resposta.json()
        except ValueError as erro:
            # Quando o BCB bloqueia ou recebe algo errado, ele devolve uma página
            # HTML em vez de JSON. Isso não é JSON — então tratamos como falha.
            raise ErroBCB("o BCB respondeu em formato inesperado") from erro

        # Às vezes o BCB responde HTTP 200 mas com um aviso de erro no corpo.
        if isinstance(dados, dict) and "erro" in dados:
            raise ErroBCB("o BCB reportou erro interno na consulta")

        return _converter(dados)
