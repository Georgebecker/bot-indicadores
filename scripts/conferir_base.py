"""Confere se a base `projeto_loop` continua presente e coerente neste projeto.

Uso:
    python scripts/conferir_base.py

Sai com codigo 0 quando tudo esta no lugar e 1 quando algo da base sumiu, divergiu
ou quando uma regra de seguranca do projeto foi violada.

Somente biblioteca padrao: roda em qualquer Python 3.8+.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE_PADRAO = Path(r"D:\Projetos\projeto_loop")
URL_BASE = "https://github.com/Georgebecker/projeto_loop"

ARQUIVOS_DO_MODELO = [
    ".gitattributes",
    ".gitignore",
    ".env.example",
    "LICENSE",
    "README.md",
    "requirements.txt",
    "AGENTS.md",
    "NOTES.md",
    "log_loop.md",
    "pytest.ini",
    "docs/REGRAS_DE_OURO.md",
    "docs/BASE_PROJETO_LOOP.md",
    ".github/copilot-instructions.md",
    ".github/agents/deepseek-flash.agent.md",
    ".github/instructions/readme-george-becker.instructions.md",
    ".github/prompts/readme.prompt.md",
    ".githooks/pre-commit",
    ".githooks/pre-push",
    ".githooks/instalar.ps1",
    ".githooks/README.md",
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/descartados/.gitkeep",
    "notebooks/.gitkeep",
    "meu-loop-agente/README.md",
    "meu-loop-agente/program.md",
    "meu-loop-agente/config_loop.json",
    "meu-loop-agente/system_prompt.md",
    "meu-loop-agente/log.md",
    "meu-loop-agente/baseline.json",
    "meu-loop-agente/verificar_iteracao.py",
    "meu-loop-agente/outputs/.gitkeep",
    "meu-loop-agente/workspace/LEIA-ME.md",
    "tests/test_base_projeto_loop.py",
]

ARQUIVOS_IDENTICOS_A_BASE = [
    "docs/REGRAS_DE_OURO.md",
    ".githooks/pre-commit",
    ".githooks/pre-push",
    ".githooks/instalar.ps1",
    ".githooks/README.md",
    ".gitattributes",
]

NOMES_DE_SEGREDO = re.compile(
    r"^(?:[A-Z0-9_]*_(?:API_KEY|SECRET|TOKEN|PASSWORD|PASSWD|DSN|PRIVATE_KEY))\s*=\s*\S+",
    re.IGNORECASE,
)

MARCA_ANCORA = "Base de trabalho"


def caminho_da_base() -> Path:
    bruto = os.getenv("PROJETO_LOOP_PATH")
    return Path(bruto) if bruto else BASE_PADRAO


def hash_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def _git(*argumentos: str) -> tuple[int, str]:
    try:
        saida = subprocess.run(
            ["git", *argumentos],
            cwd=str(RAIZ),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as erro:
        return 1, str(erro)
    return saida.returncode, (saida.stdout or saida.stderr).strip()


def linhas_de_chave_exposta(arquivo: Path) -> list[int]:
    """Numeros de linha com `NOME=valor` para nomes que parecem segredo (sem revelar o valor)."""
    if not arquivo.is_file():
        return []
    achados = []
    for numero, linha in enumerate(
        arquivo.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
    ):
        if linha.lstrip().startswith("#"):
            continue
        if NOMES_DE_SEGREDO.match(linha.strip()):
            achados.append(numero)
    return achados


def coletar_problemas(base: Path | None = None) -> list[str]:
    base = base or caminho_da_base()
    problemas: list[str] = []

    if not base.is_dir():
        problemas.append(
            f"base ausente em {base} - clone projeto_loop ai ou defina PROJETO_LOOP_PATH"
        )
        base = None

    for relativo in ARQUIVOS_DO_MODELO:
        if not (RAIZ / relativo).exists():
            problemas.append(f"arquivo do modelo ausente: {relativo}")

    if base is not None:
        for relativo in ARQUIVOS_IDENTICOS_A_BASE:
            origem = base / relativo
            destino = RAIZ / relativo
            if origem.is_file() and destino.is_file():
                if hash_arquivo(origem) != hash_arquivo(destino):
                    problemas.append(f"divergiu da base sem registro: {relativo}")
            elif origem.is_file() and not destino.is_file():
                problemas.append(f"falta copiar da base: {relativo}")

    agentes = RAIZ / "AGENTS.md"
    if agentes.is_file():
        texto = agentes.read_text(encoding="utf-8", errors="replace")
        if MARCA_ANCORA not in texto or "projeto_loop" not in texto:
            problemas.append("AGENTS.md perdeu a ancora da base (secao 'Base de trabalho')")

    ancora = RAIZ / "docs/BASE_PROJETO_LOOP.md"
    if ancora.is_file():
        texto = ancora.read_text(encoding="utf-8", errors="replace")
        if URL_BASE not in texto:
            problemas.append("docs/BASE_PROJETO_LOOP.md nao cita o repositorio da base")
        if not re.search(r"\b[0-9a-f]{40}\b", texto):
            problemas.append("docs/BASE_PROJETO_LOOP.md sem commit de referencia")

    config = RAIZ / "meu-loop-agente/config_loop.json"
    if config.is_file():
        try:
            dados = json.loads(config.read_text(encoding="utf-8"))
        except json.JSONDecodeError as erro:
            problemas.append(f"meu-loop-agente/config_loop.json invalido: {erro}")
        else:
            for chave in ("agente", "verificacao", "metrica", "limites"):
                if chave not in dados:
                    problemas.append(f"config_loop.json sem a secao '{chave}'")

    codigo, valor = _git("config", "core.hooksPath")
    if codigo != 0:
        problemas.append("git indisponivel para conferir core.hooksPath")
    elif valor.strip() != ".githooks":
        problemas.append(f"ganchos inativos: core.hooksPath={valor or '(vazio)'}")

    codigo, _ = _git("check-ignore", "-q", ".env")
    if codigo != 0:
        problemas.append("o .env nao esta sendo ignorado pelo git")

    for nome in (".env", ".env.example"):
        for numero in linhas_de_chave_exposta(RAIZ / nome):
            problemas.append(f"{nome}:{numero} parece guardar valor de chave")

    return problemas


def main() -> int:
    base = caminho_da_base()
    print(f"Base de referencia: {base}")
    problemas = coletar_problemas(base)
    if not problemas:
        print("OK: base projeto_loop conferida, nada faltando.")
        return 0
    print(f"FALHA: {len(problemas)} problema(s) encontrados.")
    for problema in problemas:
        print(f"  - {problema}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
