"""O teste que o AGENTS.md exige: a "Classificação" do README é verificável.

Por que isto existe: o README tem um quadro dizendo qual é o propósito do projeto
e o quanto ele está maduro. Quadro escrito à mão envelhece — fica "usável" mesmo
quando os testes estão vermelhos. Este teste transforma o quadro em compromisso:
se a seção sumir, ficar vazia ou declarar uma maturidade inventada, a suíte fica
vermelha e alguém precisa corrigir.
"""

from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
README = RAIZ / "README.md"

# Os quatro campos exigidos pelo AGENTS.md.
CAMPOS_OBRIGATORIOS = ("Propósito", "Maturidade", "O que está sendo treinado", "Quem usaria")

# Só estas palavras são aceitas como maturidade.
MATURIDADES_VALIDAS = {"rascunho", "funcional", "usável"}


def secao_classificacao() -> str:
    """Recorta o texto que está entre '## Classificação' e o próximo título '## '."""
    texto = README.read_text(encoding="utf-8")
    # Não confunda "re.MULTILINE" com "re.S": o DOTALL faz o ponto casar também
    # quebra de linha; é ele que permite capturar o bloco inteiro.
    casado = re.search(r"^## Classificação\s*$(.*?)(?=^## )", texto, re.MULTILINE | re.DOTALL)
    assert casado, "README.md não tem a seção '## Classificação'"
    return casado.group(1)


def test_readme_existe_com_secao_classificacao():
    """A seção precisa existir e ter conteúdo."""
    assert README.is_file()
    assert secao_classificacao().strip()


def test_classificacao_tem_os_quatro_campos_preenchidos():
    """Cada campo precisa existir e ter algo escrito de verdade (3+ caracteres)."""
    secao = secao_classificacao()
    for campo in CAMPOS_OBRIGATORIOS:
        padrao = re.compile(rf"^-\s+\*\*{re.escape(campo)}:\*\*\s*(\S.*)$", re.MULTILINE)
        casado = padrao.search(secao)
        assert casado, f"campo '{campo}' ausente na classificação"
        assert len(casado.group(1).strip()) >= 3, f"campo '{campo}' está vazio"


def test_maturidade_declarada_e_valida():
    """Maturidade só pode ser rascunho, funcional ou usável."""
    secao = secao_classificacao()
    casado = re.search(
        r"^-\s+\*\*Maturidade:\*\*\s*`?([a-záàâãéêíóôõúç]+)`?", secao, re.MULTILINE
    )
    assert casado, "campo 'Maturidade' sem valor"
    assert casado.group(1).lower() in MATURIDADES_VALIDAS, casado.group(1)


def test_classificacao_vem_antes_das_outras_secoes():
    """O leitor precisa ver a classificação no começo, não escondida no fim."""
    texto = README.read_text(encoding="utf-8")
    assert texto.index("## Classificação") < len(texto) / 3, (
        "a classificação deve aparecer no início do README"
    )
