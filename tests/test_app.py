"""Testes da montagem do bot.

Estes testes respondem a duas perguntas práticas:

1. "Os cinco comandos estão realmente ligados?" — se alguém esquecer de registrar
   um handler, o comando simplesmente não existe no Telegram, e ninguém percebe
   até um usuário reclamar.
2. "Sem token, o bot tenta conectar mesmo assim?" — não deve tentar: melhor falhar
   rápido, com explicação, do que ficar tentando sem motivo.
"""

from __future__ import annotations

from telegram.ext import CommandHandler

from bot_indicadores.app import criar_aplicacao, main


def test_aplicacao_registra_os_cinco_comandos():
    """Cada comando do contrato precisa de um handler ligado."""
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
    saida = capsys.readouterr().err
    assert "TELEGRAM_BOT_TOKEN" in saida


def test_main_com_token_invalido_falha_antes_da_rede(monkeypatch, capsys):
    """Token com formato errado também falha antes de qualquer chamada à internet."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token-sem-dois-pontos")

    assert main() == 1
    assert "TELEGRAM_BOT_TOKEN" in capsys.readouterr().err
