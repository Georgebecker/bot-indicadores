"""Testes das mensagens que o bot envia e da montagem da aplicação.

Aqui não usamos Telegram de verdade: criamos um "mensageiro falso" que só anota o
texto que receberia. Depois conferimos se o texto está certo — com o número, a
data e a fonte — e se, quando o Banco Central falha, o usuário recebe uma
mensagem educada em vez de um erro técnico.

No fim do arquivo ficam os testes de montagem: eles respondem "os cinco comandos
estão realmente ligados?" e "sem token o bot tenta conectar mesmo assim?".
"""

from __future__ import annotations

from datetime import date

from telegram.ext import CommandHandler

from bot_indicadores.app import criar_aplicacao, main
from bot_indicadores.bcb import ErroBCB, Ponto
from bot_indicadores.handlers import (
    MENSAGEM_BOAS_VINDAS,
    MENSAGEM_ERRO,
    ComandosIndicadores,
)


class MensagemFalsa:
    """Finge ser a mensagem do Telegram: guarda o que seria enviado."""

    def __init__(self):
        self.respostas: list[str] = []

    async def reply_text(self, texto):
        self.respostas.append(texto)


class UpdateFalso:
    """Finge ser o "pacote" que chega quando alguém manda uma mensagem."""

    def __init__(self):
        self.message = MensagemFalsa()


class ClienteFalso:
    """Finge ser o cliente do Banco Central, devolvendo valores prontos."""

    def __init__(self, pontos_por_codigo=None, erro=False):
        self._pontos = pontos_por_codigo or {}
        self._erro = erro
        # Guarda o que foi pedido, para conferir se o IPCA pediu 12 valores.
        self.pedidos: list[tuple[int, int]] = []

    async def ultimos(self, codigo, quantidade=1):
        self.pedidos.append((codigo, quantidade))
        if self._erro:
            raise ErroBCB("API fora do ar")
        return self._pontos[codigo]


def cliente_padrao():
    """Um Banco Central de mentira com valores fáceis de conferir."""
    return ClienteFalso(
        {
            1: [Ponto(date(2026, 10, 1), 5.2079)],  # dólar
            432: [Ponto(date(2026, 10, 1), 13.75)],  # Selic
            # Doze meses de 0,44% para conferir o acumulado (deve dar 5,41%).
            433: [Ponto(date(2025, 11, 1), 0.44)] * 11
            + [Ponto(date(2026, 9, 1), 0.44)],
            195: [Ponto(date(2026, 10, 1), 0.50)],  # poupança
        }
    )


# ---------------------------------------------------------------------------
# Boas-vindas
# ---------------------------------------------------------------------------

async def test_start_lista_os_quatro_comandos():
    """Quem chega precisa saber, de cara, o que pode pedir."""
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).start(update, None)
    texto = update.message.respostas[0]
    assert texto == MENSAGEM_BOAS_VINDAS
    for comando in ("/dolar", "/selic", "/ipca", "/poupanca"):
        assert comando in texto


# ---------------------------------------------------------------------------
# Cada comando devolve o número certo, com data e fonte
# ---------------------------------------------------------------------------

async def test_dolar_mostra_valor_e_data_de_referencia():
    """Dólar: valor em reais (vírgula), data no formato brasileiro e fonte."""
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).dolar(update, None)
    texto = update.message.respostas[0]
    assert "R$ 5,2079" in texto
    assert "01/10/2026" in texto
    assert "SGS 1" in texto


async def test_selic_mostra_percentual_ao_ano():
    """Selic é taxa anual — dizer "ao ano" evita confusão com a poupança."""
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).selic(update, None)
    texto = update.message.respostas[0]
    assert "13,75% ao ano" in texto
    assert "SGS 432" in texto


async def test_ipca_acumula_doze_meses():
    """IPCA mostra o acumulado e o último mês — e pede 12 valores, não 1."""
    cliente = cliente_padrao()
    update = UpdateFalso()
    await ComandosIndicadores(cliente).ipca(update, None)
    texto = update.message.respostas[0]
    assert "5,41% em 12 meses" in texto
    assert "Último mês (09/2026): 0,44%" in texto
    assert cliente.pedidos == [(433, 12)]


async def test_poupanca_mostra_percentual_ao_mes():
    """Poupança é mensal; por isso o texto diz "ao mês"."""
    update = UpdateFalso()
    await ComandosIndicadores(cliente_padrao()).poupanca(update, None)
    texto = update.message.respostas[0]
    assert "0,50% ao mês" in texto
    assert "SGS 195" in texto
    assert "01/10/2026" in texto


# ---------------------------------------------------------------------------
# Quando o Banco Central falha
# ---------------------------------------------------------------------------

async def test_falha_da_api_responde_mensagem_amigavel():
    """Falha vira frase simples — sem stack trace e sem nome técnico de erro."""
    update = UpdateFalso()
    await ComandosIndicadores(ClienteFalso(erro=True)).dolar(update, None)
    assert update.message.respostas == [MENSAGEM_ERRO]
    assert "Traceback" not in update.message.respostas[0]
    assert "ErroBCB" not in update.message.respostas[0]


async def test_falha_da_api_nao_vaza_excecao_no_chat_em_nenhum_comando():
    """A garantia vale para os quatro comandos, não só para o dólar."""
    for nome in ("dolar", "selic", "ipca", "poupanca"):
        update = UpdateFalso()
        comandos = ComandosIndicadores(ClienteFalso(erro=True))
        await getattr(comandos, nome)(update, None)
        assert update.message.respostas == [MENSAGEM_ERRO], nome


# ---------------------------------------------------------------------------
# Montagem: os comandos estão ligados e o bot falha cedo sem token
# ---------------------------------------------------------------------------

def test_aplicacao_registra_os_cinco_comandos():
    """Cada comando do contrato precisa de um handler ligado.

    Se alguém esquecer de registrar um handler, o comando simplesmente não existe no
    Telegram — e ninguém percebe até um usuário reclamar.
    """
    aplicacao = criar_aplicacao("123456:TOKEN-DE-TESTE")

    # A aplicação guarda os handlers em grupos (o primeiro grupo é o principal).
    grupos = aplicacao.handlers[0]

    # Para cada handler que é de comando, pegamos os nomes que ele atende.
    comandos = {
        comando
        for handler in grupos
        if isinstance(handler, CommandHandler)
        for comando in handler.commands
    }
    assert comandos == {"start", "dolar", "selic", "ipca", "poupanca"}


def test_main_sem_token_falha_sem_tentar_conectar(monkeypatch, capsys):
    """"Sem token" precisa terminar com código 1 e uma explicação no aviso (stderr)."""
    # `monkeypatch` remove a variável só durante este teste; depois ela volta.
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    assert main() == 1

    # `capsys` captura o que seria impresso na tela.
    assert "TELEGRAM_BOT_TOKEN" in capsys.readouterr().err


def test_main_com_token_invalido_falha_antes_da_rede(monkeypatch, capsys):
    """Token com formato errado também falha antes de qualquer chamada à internet."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token-sem-dois-pontos")

    assert main() == 1
    assert "TELEGRAM_BOT_TOKEN" in capsys.readouterr().err
