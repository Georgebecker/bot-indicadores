# workspace — campo de ação do agente

Pasta herdada da base `projeto_loop`: é aqui que o agente de Loop Engineering escreve.

- **Hoje está vazia de propósito.** O contrato do produto ainda não chegou, então não há
  sistema alvo para colocar aqui.
- Enquanto o contrato não chega, o escopo permitido está em
  [`../program.md`](../program.md) e aponta para `tests/`, `scripts/`, `docs/`,
  `README.md`, `NOTES.md` e `log_loop.md` — não para esta pasta.
- Quando o contrato chegar, o sistema alvo entra aqui e `program.md` +
  `config_loop.json` são ajustados pelo humano.
- Tudo aqui pode ser alterado ou revertido a cada iteração. Use Git para ter pontos de
  retorno (commit antes de cada iteração).
- Não coloque segredos (`.env`, chaves, credenciais) aqui.
