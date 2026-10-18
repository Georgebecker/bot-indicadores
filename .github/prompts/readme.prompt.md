---
description: "Gera ou atualiza o README.md no padrão George Becker: gancho claro, ## Classificação, metodologia Loop, convite a PRs e limitações honestas."
name: "README padrão George Becker"
argument-hint: "Ex.: atualizar o README com a nova funcionalidade de X"
agent: "agent"
tools: [read, search, edit, execute]
---

Leia [`.github/instructions/readme-george-becker.instructions.md`](../instructions/readme-george-becker.instructions.md)
e siga a estrutura dela à risca.

1. Leia o código e os documentos do projeto (`AGENTS.md`, `NOTES.md`, `log_loop.md`)
   e extraia **apenas** as funcionalidades que existem de fato.
2. Escreva o `README.md` na ordem: cabeçalho e gancho → `## Classificação` (quatro
   campos, coerentes com o estado real) → metodologia Loop → o que tem aqui →
   como rodar → 🚀 convite à interação → transparência e limitações → tags.
3. Mantenha o texto em português do Brasil, na primeira pessoa, direto e transparente,
   com no máximo ~150 linhas.
4. Nada de URL, chave PIX, badge de status ou funcionalidade inventada.
5. Ao terminar, mostre o que mudou e sugira **3 títulos de Issue** terminando com
   `[good first issue]`.
