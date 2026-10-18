"""O teste que o AGENTS.md exige: a classificação do README é verificável."""

from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
README = RAIZ / "README.md"

CAMPOS_OBRIGATORIOS = ("Propósito", "Maturidade", "O que está sendo treinado", "Quem usaria")
MATURIDADES_VALIDAS = {"rascunho", "funcional", "usável"}


def secao_classificacao() -> str:
    texto = README.read_text(encoding="utf-8")
    casado = re.search(r"^## Classificação\s*$(.*?)(?=^## )", texto, re.MULTILINE | re.DOTALL)
    assert casado, "README.md não tem a seção '## Classificação'"
    return casado.group(1)


def test_readme_existe_com_secao_classificacao():
    assert README.is_file()
    assert secao_classificacao().strip()


def test_classificacao_tem_os_quatro_campos_preenchidos():
    secao = secao_classificacao()
    for campo in CAMPOS_OBRIGATORIOS:
        padrao = re.compile(rf"^-\s+\*\*{re.escape(campo)}:\*\*\s*(\S.*)$", re.MULTILINE)
        casado = padrao.search(secao)
        assert casado, f"campo '{campo}' ausente na classificação"
        assert len(casado.group(1).strip()) >= 3, f"campo '{campo}' está vazio"


def test_maturidade_declarada_e_valida():
    secao = secao_classificacao()
    casado = re.search(r"^-\s+\*\*Maturidade:\*\*\s*`?([a-záàâãéêíóôõúç]+)`?", secao, re.MULTILINE)
    assert casado, "campo 'Maturidade' sem valor"
    assert casado.group(1).lower() in MATURIDADES_VALIDAS, casado.group(1)


def test_classificacao_vem_antes_das_outras_secoes():
    texto = README.read_text(encoding="utf-8")
    assert texto.index("## Classificação") < len(texto) / 3, (
        "a classificação deve aparecer no início do README"
    )
