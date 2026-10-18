"""Testes de montagem da aplicação e da inicialização sem token."""

from __future__ import annotations

import pytest
from telegram.ext import CommandHandler

from bot_indicadores.app import criar_aplicacao, main


def test_aplicacao_registra_os_cinco_comandos():
    aplicacao = criar_aplicacao("123456:TOKEN-DE-TESTE")
    grupos = aplicacao.handlers[0]
    comandos = {comando for h in grupos if isinstance(h, CommandHandler) for comando in h.commands}
    assert comandos == {"start", "dolar", "selic", "ipca", "poupanca"}


def test_main_sem_token_falha_sem_tentar_conectar(monkeypatch, capsys):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    assert main() == 1
    saida = capsys.readouterr().err
    assert "TELEGRAM_BOT_TOKEN" in saida


def test_main_com_token_invalido_falha_antes_da_rede(monkeypatch, capsys):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token-sem-dois-pontos")
    assert main() == 1
    assert "TELEGRAM_BOT_TOKEN" in capsys.readouterr().err
