"""Guardas de segredo: o `.env` nunca sobe e nenhum valor de chave fica versionado.

Estes testes não precisam de rede nem de token. Eles falham de propósito se:
- o `.env` deixar de ser ignorado pelo git ou entrar no índice;
- algum arquivo versionado tiver `NOME_DE_CHAVE=valor` preenchido;
- algum arquivo versionado contiver o valor real de uma chave da máquina.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent

NOMES_DE_CHAVE = re.compile(
    r"^\s*(?:export\s+)?([A-Z0-9_]*(?:API_KEY|APIKEY|TOKEN|SECRET|PASSWORD|PASSWD|DSN|PRIVATE_KEY|CREDENTIAL)[A-Z0-9_]*)"
    r"\s*=\s*(.+)$"
)

PREFIXOS_DE_CHAVE = (
    "sk-",
    "sk-proj-",
    "ghp_",
    "gho_",
    "github_pat_",
    "hf_",
    "AIza",
    "AKIA",
    "xoxb-",
    "xoxp-",
)

# 123456789:AA... (token do BotFather) e JWT
FORMATOS_DE_CHAVE = (
    re.compile(r"^\d{6,12}:[A-Za-z0-9_-]{20,}$"),
    re.compile(r"^eyJ[A-Za-z0-9_-]{10,}\."),
)

CHAVES_DA_MAQUINA = (
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_API_KEY_BOT_INDICADORES",
    "DEEPSEEK_API_KEY_RIGELLLM",
    "OPENAI_API_KEY",
    "HF_TOKEN",
    "PEXELS_API_KEY",
    "TELEGRAM_BOT_TOKEN",
    "GOOGLE_API_KEY",
    "ANTHROPIC_API_KEY",
)

TAMANHO_MINIMO_DE_SEGREDO = 12


def git(*argumentos: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *argumentos],
        cwd=str(RAIZ),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )


def arquivos_rastreados() -> list[str]:
    saida = git("ls-files")
    if saida.returncode != 0:
        pytest.skip("git indisponível para a conferência de segredos")
    return [linha for linha in saida.stdout.splitlines() if linha.strip()]


def ler_texto(relativo: str) -> str | None:
    caminho = RAIZ / relativo
    try:
        return caminho.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return None


def valor_no_ambiente(nome: str) -> str | None:
    """Lê do processo e, no Windows, do registro (variável do usuário)."""
    valor = os.environ.get(nome)
    if valor:
        return valor
    if sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as chave:
                return winreg.QueryValueEx(chave, nome)[0]
        except (OSError, ImportError):
            return None
    return None


def test_env_nao_esta_versionado():
    rastreados = arquivos_rastreados()
    perigosos = [nome for nome in rastreados if Path(nome).name == ".env"]
    assert perigosos == [], f".env entrou no índice: {perigosos}"


def test_env_e_ignorado_pelo_git():
    assert git("check-ignore", "-q", ".env").returncode == 0, (
        ".env deixou de ser ignorado pelo .gitignore"
    )


def test_variantes_do_env_tambem_sao_ignoradas():
    for nome in (".env.local", ".env.prod", ".env.bak"):
        assert git("check-ignore", "-q", nome).returncode == 0, f"{nome} pode subir por engano"


def test_env_example_e_versionavel():
    assert git("check-ignore", "-q", ".env.example").returncode != 0, (
        ".env.example precisa continuar versionável (é o modelo sem valores)"
    )
    assert ".env.example" in arquivos_rastreados()


def parece_segredo(valor: str) -> bool:
    """Distingue credencial de constante: nome em MAIÚSCULAS não é segredo."""
    limpo = valor.strip().strip("\"'").strip()
    if len(limpo) < TAMANHO_MINIMO_DE_SEGREDO:
        return False
    if limpo.startswith(PREFIXOS_DE_CHAVE):
        return True
    if any(formato.match(limpo) for formato in FORMATOS_DE_CHAVE):
        return True
    tem_letra = any(c.isalpha() for c in limpo)
    tem_digito = any(c.isdigit() for c in limpo)
    return tem_letra and tem_digito


def test_nenhum_arquivo_versionado_tem_valor_de_chave():
    problemas: list[str] = []
    for relativo in arquivos_rastreados():
        texto = ler_texto(relativo)
        if texto is None:
            continue
        for numero, linha in enumerate(texto.splitlines(), start=1):
            if linha.lstrip().startswith("#"):
                continue
            casado = NOMES_DE_CHAVE.match(linha)
            if casado and parece_segredo(casado.group(2)):
                problemas.append(f"{relativo}:{numero} -> {casado.group(1)}")
    assert problemas == [], "valor de chave em arquivo versionado: " + ", ".join(problemas)


def test_nenhum_arquivo_versionado_contem_o_valor_de_uma_chave_da_maquina():
    segredos = {
        nome: valor
        for nome in CHAVES_DA_MAQUINA
        if (valor := valor_no_ambiente(nome)) and len(valor) >= TAMANHO_MINIMO_DE_SEGREDO
    }
    if not segredos:
        pytest.skip("nenhuma chave visível neste processo para comparar")

    vazamentos: list[str] = []
    for relativo in arquivos_rastreados():
        caminho = RAIZ / relativo
        try:
            conteudo = caminho.read_bytes()
        except OSError:
            continue
        for nome, valor in segredos.items():
            if valor.encode("utf-8") in conteudo:
                vazamentos.append(f"{relativo} contém {nome}")
    assert vazamentos == [], "segredo encontrado: " + ", ".join(vazamentos)
