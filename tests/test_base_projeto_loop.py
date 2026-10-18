"""Testes da ancora com a base `projeto_loop`.

Se a base sumir, divergir ou o AGENTS.md perder a secao "Base de trabalho",
a suite fica vermelha de proposito: e o lembrete permanente.
"""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ_CONFERIDOR = RAIZ / "scripts" / "conferir_base.py"


def carregar_conferidor():
    especificacao = importlib.util.spec_from_file_location("conferir_base", ARQ_CONFERIDOR)
    modulo = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(modulo)
    return modulo


class BaseProjetoLoopTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conferidor = carregar_conferidor()

    def test_conferidor_existe(self):
        self.assertTrue(ARQ_CONFERIDOR.is_file(), "scripts/conferir_base.py sumiu")

    def test_base_completa_sem_problemas(self):
        problemas = self.conferidor.coletar_problemas()
        self.assertEqual(problemas, [], "base projeto_loop com pendencias:\n" + "\n".join(problemas))

    def test_agentes_mantem_ancora_da_base(self):
        texto = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(self.conferidor.MARCA_ANCORA, texto)
        self.assertIn("projeto_loop", texto)

    def test_documento_da_base_cita_origem(self):
        texto = (RAIZ / "docs" / "BASE_PROJETO_LOOP.md").read_text(encoding="utf-8")
        self.assertIn(self.conferidor.URL_BASE, texto)

    def test_config_do_loop_aponta_para_o_projeto(self):
        config = json.loads(
            (RAIZ / "meu-loop-agente" / "config_loop.json").read_text(encoding="utf-8")
        )
        diretorio = (RAIZ / "meu-loop-agente" / config["verificacao"]["diretorio_de_trabalho"]).resolve()
        self.assertEqual(diretorio, RAIZ.resolve())
        self.assertIn("pytest", " ".join(config["verificacao"]["comandos"]))

    def test_nenhum_valor_de_chave_em_arquivo(self):
        for nome in (".env", ".env.example"):
            self.assertEqual(
                self.conferidor.linhas_de_chave_exposta(RAIZ / nome),
                [],
                f"{nome} parece guardar valor de chave",
            )


if __name__ == "__main__":
    unittest.main()
