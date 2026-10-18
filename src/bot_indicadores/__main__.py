"""Permite rodar o bot com `python -m bot_indicadores`.

O `-m` diz ao Python: "procure um pacote com este nome e execute o `__main__.py`".
É um atalho para não precisar escrever o caminho completo do arquivo.
"""

from .app import main

# Este `if` só é verdadeiro quando o arquivo é executado diretamente.
# `raise SystemExit(main())` encerra o programa com o código devolvido por `main`
# (0 = deu tudo certo, 1 = faltou configuração).
if __name__ == "__main__":
    raise SystemExit(main())
