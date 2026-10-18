# log_loop.md — bot-indicadores

Cada ciclo segue o mesmo formato: hipótese, mudança, arquivos, métrica antes/depois,
verificação e decisão (ACEITO mantém; REJEITADO reverte). A linha de base só avança
com melhoria medida e suíte verde.

## Linha de base

- Sem código, sem testes e sem métrica principal definida.
- Aguardando o contrato/prompt do projeto.

## Ciclos

### Ciclo 0 — persona do agente (infraestrutura, sem métrica de produto)

- **Hipótese:** fixar a persona do agente em arquivo versionado evita repetir as regras
  de `AGENTS.md` a cada sessão e reduz desvio de idioma, segredo e método.
- **Mudança:** `.github/agents/deepseek-flash.agent.md` com modelo
  `deepseek/deepseek-v4-flash`, esforço alto, ferramentas mínimas e restrições do projeto.
- **Arquivos:** `.github/agents/deepseek-flash.agent.md`, `NOTES.md`, `log_loop.md`.
- **Métrica:** sem métrica de produto; verificação = frontmatter YAML válido e arquivo
  reconhecido em `.github/agents/`.
- **Decisão:** ACEITO — persona entra na linha de base; nenhum código de produto.

### Ciclo 1 — instrução de README (infraestrutura, sem métrica de produto)

- **Hipótese:** registrar o padrão de README como instrução de arquivo
  (`applyTo: "**/README.md"`) mantém o padrão disponível na hora certa sem consumir
  contexto nas tarefas de código nem alterar o ciclo do Loop Engineering.
- **Mudança:** `.github/instructions/readme-george-becker.instructions.md` e um ponteiro
  no agente `deepseek-flash`.
- **Arquivos:** `.github/instructions/readme-george-becker.instructions.md`,
  `.github/agents/deepseek-flash.agent.md`, `NOTES.md`, `log_loop.md`.
- **Métrica:** sem métrica de produto; verificação = frontmatter YAML válido, `applyTo`
  correto e `README.md` atual ainda com a seção `## Classificação`.
- **Decisão:** ACEITO — instrução entra na linha de base; nenhum código de produto.

### Ciclo 2 — README no padrão George Becker (documentação)

- **Hipótese:** um README com gancho, convite a PRs e limitações explícitas aumenta a
  interação (issues e PRs) sem inflar o documento nem prometer o que não existe.
- **Mudança:** `README.md` reescrito na ordem do padrão (cabeçalho/badges → gancho →
  `## Classificação` → metodologia Loop → o que tem aqui → como rodar → convite →
  limitações → tags → licença). Criado `.github/prompts/readme.prompt.md` para reuso.
- **Arquivos:** `README.md`, `.github/prompts/readme.prompt.md`, `NOTES.md`, `log_loop.md`.
- **Métrica:** sem métrica de produto; verificação = `## Classificação` presente com os
  quatro campos, README com ~110 linhas (limite ~150) e nenhuma funcionalidade inventada.
- **Decisão:** ACEITO — README novo entra na linha de base.

Nenhum ciclo de produto executado. O primeiro só começa depois que o contrato definir o
sistema alvo e a métrica principal.
