"""Testes da âncora com a base `projeto_loop`.

Pense neste arquivo como um alarme. Se a base do método sumir, se as Regras de Ouro
forem apagadas ou se o `AGENTS.md` deixar de avisar de onde o projeto vem, o alarme
toca (a suíte fica vermelha) em vez de o esquecimento passar despercebido.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ_CONFERIDOR = RAIZ / "scripts" / "conferir_base.py"


def carregar_conferidor():
    """Carrega `scripts/conferir_base.py` como módulo, mesmo ele não sendo um pacote.

    `importlib` é o mecanismo que carrega código a partir do caminho do arquivo.
    """
    especificacao = importlib.util.spec_from_file_location("conferir_base", ARQ_CONFERIDOR)
    modulo = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(modulo)
    return modulo


class BaseProjetoLoopTest(unittest.TestCase):
    """Usamos `unittest` aqui porque não precisamos de nada assíncrono."""

    @classmethod
    def setUpClass(cls):
        # Roda uma vez só, antes de todos os testes da classe.
        cls.conferidor = carregar_conferidor()

    def test_conferidor_existe(self):
        """O zelador da base precisa existir para poder ser executado."""
        self.assertTrue(ARQ_CONFERIDOR.is_file(), "scripts/conferir_base.py sumiu")

    def test_base_completa_sem_problemas(self):
        """A ronda completa não deve encontrar nenhum problema."""
        problemas = self.conferidor.coletar_problemas()
        self.assertEqual(
            problemas, [], "base projeto_loop com pendencias:\n" + "\n".join(problemas)
        )

    def test_agentes_mantem_ancora_da_base(self):
        """O AGENTS.md precisa continuar dizendo de onde o projeto vem."""
        texto = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(self.conferidor.MARCA_ANCORA, texto)
        self.assertIn("projeto_loop", texto)

    def test_referencia_da_base_cita_origem(self):
        """A URL do repositório original continua escrita no AGENTS.md."""
        texto = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(self.conferidor.URL_BASE, texto)

    def test_nenhum_valor_de_chave_em_arquivo(self):
        """O `.env.example` (versionado) nunca guarda valor de chave.

        O `.env` **não** é auditado: ele é local, pertence ao dono e pode guardar o
        valor — desde que nunca suba (os testes de `test_segredos.py` garantem isso).
        """
        self.assertEqual(
            self.conferidor.linhas_de_chave_exposta(RAIZ / ".env.example"),
            [],
            ".env.example parece guardar valor de chave",
        )


if __name__ == "__main__":
    # Permite rodar este arquivo sozinho: python tests/test_base_projeto_loop.py
    unittest.main()
