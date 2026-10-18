"""Confere se a base `projeto_loop` continua presente e coerente neste projeto.

Pense neste arquivo como o **zelador** do projeto: ele faz uma ronda de poucos
segundos e anota tudo que está errado. Ele não conserta nada sozinho — só avisa.

Por que ele existe: o projeto nasce de um modelo (`projeto_loop`). Se alguém apagar
as Regras de Ouro, desligar os ganchos de segurança ou deixar uma chave dentro de um
arquivo, o zelador percebe antes de o problema virar prejuízo.

Como usar:

    python scripts/conferir_base.py

Ele responde "OK" e termina com código 0 quando está tudo certo.
Qualquer outro código (1) significa "achado problema" — e ele lista cada um.

Os dados são conferidos em duas camadas:
1. **Local**: o que está neste projeto (arquivos, ganchos, `.env` ignorado).
2. **Comparação com a base**: se o clone do `projeto_loop` estiver na máquina,
   compara o conteúdo dos arquivos que devem ser cópias fiéis.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Onde ficam as coisas
# ---------------------------------------------------------------------------

# A raiz do projeto é a pasta que fica um nível acima de `scripts/`.
# `__file__` é este arquivo; `.parent` sobe um nível; `.parent.parent` sobe dois.
RAIZ = Path(__file__).resolve().parent.parent

# Onde o modelo costuma estar clonado nesta máquina.
# Dá para apontar outro lugar com a variável de ambiente PROJETO_LOOP_PATH.
BASE_PADRAO = Path(r"D:\Projetos\projeto_loop")
URL_BASE = "https://github.com/Georgebecker/projeto_loop"

# Arquivos que sempre precisam existir neste projeto.
# Se um deles desaparecer, é sinal de que alguém apagou parte do método ou do produto.
ARQUIVOS_DO_MODELO = [
    # --- raiz do projeto ---
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
    # --- documentação do método ---
    "docs/REGRAS_DE_OURO.md",
    "docs/BASE_PROJETO_LOOP.md",
    # --- customizações do agente/editor ---
    ".github/copilot-instructions.md",
    ".github/instructions/readme-george-becker.instructions.md",
    ".github/prompts/readme.prompt.md",
    # --- segurança (ganchos do git) ---
    ".githooks/pre-commit",
    ".githooks/pre-push",
    ".githooks/instalar.ps1",
    ".githooks/README.md",
    # --- pastas de dados (vazias por enquanto, só com o marcador .gitkeep) ---
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/descartados/.gitkeep",
    "notebooks/.gitkeep",
    # --- o loop operacional (contrato, métrica e verificador) ---
    "meu-loop-agente/README.md",
    "meu-loop-agente/program.md",
    "meu-loop-agente/config_loop.json",
    "meu-loop-agente/system_prompt.md",
    "meu-loop-agente/log.md",
    "meu-loop-agente/baseline.json",
    "meu-loop-agente/verificar_iteracao.py",
    "meu-loop-agente/outputs/.gitkeep",
    "meu-loop-agente/workspace/LEIA-ME.md",
    # --- testes da própria âncora ---
    "tests/test_base_projeto_loop.py",
]

# Arquivos que devem ser cópia fiel da base, conferidos byte a byte (hash).
ARQUIVOS_IDENTICOS_A_BASE = [
    ".githooks/pre-commit",
    ".githooks/pre-push",
    ".githooks/instalar.ps1",
    ".githooks/README.md",
    ".gitattributes",
]

# Arquivo que PODE crescer em relação à base (com acréscimo no final), mas nunca
# perder ou alterar o conteúdo original. As Regras de Ouro ganharam a "Parte V —
# Didática obrigatória" deste projeto, então o original precisa continuar intacto
# no começo do arquivo.
ARQUIVOS_COM_ACRESCIMO_PERMITIDO = [
    "docs/REGRAS_DE_OURO.md",
]

# Um "nome de chave" é algo como DEEPSEEK_API_KEY, TELEGRAM_BOT_TOKEN, HF_TOKEN...
# Este padrão procura linhas no formato NOME_DE_CHAVE=algum valor.
NOMES_DE_SEGREDO = re.compile(
    r"^(?:[A-Z0-9_]*_(?:API_KEY|SECRET|TOKEN|PASSWORD|PASSWD|DSN|PRIVATE_KEY))\s*=\s*\S+",
    re.IGNORECASE,
)

# Esta frase precisa existir no AGENTS.md: é a placa que lembra o agente da base.
MARCA_ANCORA = "Base de trabalho"


# ---------------------------------------------------------------------------
# Utilidades pequenas (funções de apoio, sem regra de negócio)
# ---------------------------------------------------------------------------

def caminho_da_base() -> Path:
    """Devolve onde procurar o clone da base (variável de ambiente ou o padrão)."""
    bruto = os.getenv("PROJETO_LOOP_PATH")
    return Path(bruto) if bruto else BASE_PADRAO


def hash_arquivo(caminho: Path) -> str:
    """Calcula uma 'impressão digital' do arquivo (SHA-256).

    Dois arquivos com o mesmo hash têm exatamente o mesmo conteúdo. É assim que
    comparamos sem precisar abrir e ler tudo linha por linha.
    """
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def _git(*argumentos: str) -> tuple[int, str]:
    """Roda um comando do git e devolve (código de saída, texto da resposta)."""
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
    """Devolve os números das linhas que parecem guardar valor de chave.

    Nunca devolvemos o valor em si — apenas "a linha 12 está suspeita".
    Linhas que começam com # são comentários e ficam de fora.
    """
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


# ---------------------------------------------------------------------------
# A ronda de conferência
# ---------------------------------------------------------------------------

def coletar_problemas(base: Path | None = None) -> list[str]:
    """Faz todas as conferências e devolve a lista de problemas encontrados.

    Lista vazia = está tudo certo. Cada item é uma frase explicando o que falhou.
    """
    base = base or caminho_da_base()
    problemas: list[str] = []

    # 1. A base está clonada nesta máquina?
    #    (Sem ela, as comparações de conteúdo não podem acontecer.)
    if not base.is_dir():
        problemas.append(
            f"base ausente em {base} - clone projeto_loop ai ou defina PROJETO_LOOP_PATH"
        )
        base = None

    # 2. Todos os arquivos do modelo existem aqui?
    for relativo in ARQUIVOS_DO_MODELO:
        if not (RAIZ / relativo).exists():
            problemas.append(f"arquivo do modelo ausente: {relativo}")

    # 3. Os arquivos que devem ser cópia fiel continuam iguais?
    if base is not None:
        for relativo in ARQUIVOS_IDENTICOS_A_BASE:
            origem = base / relativo
            destino = RAIZ / relativo
            if origem.is_file() and destino.is_file():
                if hash_arquivo(origem) != hash_arquivo(destino):
                    problemas.append(f"divergiu da base sem registro: {relativo}")
            elif origem.is_file() and not destino.is_file():
                problemas.append(f"falta copiar da base: {relativo}")

        # 4. Arquivos que podem ganhar texto no final, mas não podem perder o original.
        for relativo in ARQUIVOS_COM_ACRESCIMO_PERMITIDO:
            origem = base / relativo
            destino = RAIZ / relativo
            if not (origem.is_file() and destino.is_file()):
                continue
            texto_base = origem.read_text(encoding="utf-8", errors="replace").strip()
            texto_local = destino.read_text(encoding="utf-8", errors="replace").strip()
            if not texto_local.startswith(texto_base):
                problemas.append(
                    f"{relativo} alterou o conteúdo da base (acréscimo no final é permitido;"
                    " edição do original, não)"
                )

    # 5. O AGENTS.md ainda avisa que o projeto vem da base?
    agentes = RAIZ / "AGENTS.md"
    if agentes.is_file():
        texto = agentes.read_text(encoding="utf-8", errors="replace")
        if MARCA_ANCORA not in texto or "projeto_loop" not in texto:
            problemas.append("AGENTS.md perdeu a ancora da base (secao 'Base de trabalho')")

    # 6. O documento da base cita o repositório e o commit de referência?
    ancora = RAIZ / "docs/BASE_PROJETO_LOOP.md"
    if ancora.is_file():
        texto = ancora.read_text(encoding="utf-8", errors="replace")
        if URL_BASE not in texto:
            problemas.append("docs/BASE_PROJETO_LOOP.md nao cita o repositorio da base")
        if not re.search(r"\b[0-9a-f]{40}\b", texto):
            problemas.append("docs/BASE_PROJETO_LOOP.md sem commit de referencia")

    # 7. O contrato do loop tem as quatro seções que o verificador espera?
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

    # 8. Os ganchos de segurança estão ativos neste clone?
    #    (Eles são o que impede o .env de chegar ao GitHub.)
    codigo, valor = _git("config", "core.hooksPath")
    if codigo != 0:
        problemas.append("git indisponivel para conferir core.hooksPath")
    elif valor.strip() != ".githooks":
        problemas.append(f"ganchos inativos: core.hooksPath={valor or '(vazio)'}")

    # 9. O git está de fato ignorando o .env?
    codigo, _ = _git("check-ignore", "-q", ".env")
    if codigo != 0:
        problemas.append("o .env nao esta sendo ignorado pelo git")

    # 10. Algum arquivo de configuração guarda valor de chave?
    for nome in (".env", ".env.example"):
        for numero in linhas_de_chave_exposta(RAIZ / nome):
            problemas.append(f"{nome}:{numero} parece guardar valor de chave")

    return problemas


def main() -> int:
    """Mostra o resultado da ronda. Código 0 = tudo certo; 1 = tem problema."""
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


# Este bloco só roda quando alguém executa o arquivo direto (python scripts/...).
# Quando outro arquivo faz "import", ele não roda.
if __name__ == "__main__":
    sys.exit(main())
