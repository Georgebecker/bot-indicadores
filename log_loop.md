# log_loop.md — bot-indicadores

Cada ciclo segue o mesmo formato: hipótese, mudança, arquivos, métrica antes/depois,
verificação e decisão (ACEITO mantém; REJEITADO reverte). A linha de base só avança
com melhoria medida e suíte verde.

## Linha de base

- Métrica do loop: **43 testes que passam** (`.venv\Scripts\python.exe -m pytest`),
  registrada em `meu-loop-agente/baseline.json` (valor inicial 6, melhor 43).
- Bot de Telegram entregue no escopo do contrato v1.0.

## Ciclos

### Ciclo 0 — persona do agente (infraestrutura, sem métrica de produto)

- **Hipótese:** fixar a persona do agente em arquivo local evita repetir as regras
  de `AGENTS.md` a cada sessão e reduz desvio de idioma, segredo e método.
- **Mudança:** persona de desenvolvimento com ferramentas mínimas e restrições do projeto.
- **Arquivos:** persona local (fora do repositório, por decisão posterior do dono),
  `NOTES.md`, `log_loop.md`.
- **Métrica:** sem métrica de produto; verificação = frontmatter YAML válido.
- **Decisão:** ACEITO — persona entra na linha de base; nenhum código de produto.

### Ciclo 1 — instrução de README (infraestrutura, sem métrica de produto)

- **Hipótese:** registrar o padrão de README como instrução de arquivo
  (`applyTo: "**/README.md"`) mantém o padrão disponível na hora certa sem consumir
  contexto nas tarefas de código nem alterar o ciclo do Loop Engineering.
- **Mudança:** `.github/instructions/readme-george-becker.instructions.md` e um ponteiro
  na persona local.
- **Arquivos:** `.github/instructions/readme-george-becker.instructions.md`, `NOTES.md`,
  `log_loop.md`.
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

### Ciclo 3 — sincronizar a base `projeto_loop` (infraestrutura)

- **Hipótese:** se a base do método viver no repositório (arquivos + conferência
  executável + teste), o agente deixa de depender da memória da sessão e para de esquecer
  as Regras de Ouro e o próprio loop.
- **Mudança:** cópia de `.gitattributes`, `requirements.txt` e `meu-loop-agente/`
  (adaptado para `python -m pytest` como métrica provisória); criação de
  `docs/BASE_PROJETO_LOOP.md`, `scripts/conferir_base.py` e
  `tests/test_base_projeto_loop.py`; âncora no topo de `AGENTS.md` e em
  `.github/copilot-instructions.md`.
- **Arquivos:** `AGENTS.md`, `docs/BASE_PROJETO_LOOP.md`, `scripts/conferir_base.py`,
  `tests/test_base_projeto_loop.py`, `meu-loop-agente/**`, `requirements.txt`,
  `.gitattributes`, `.gitignore`, `README.md`, `NOTES.md`, `log_loop.md`.
- **Métrica antes:** 0 testes passando. **Depois:** 6 testes passando
  (`python -m pytest`), linha de base gravada em `baseline.json`.
- **Verificação:** `python scripts/conferir_base.py` sai com código 0; nenhum valor de
  chave encontrado em `.env`/`.env.example`.
- **Decisão:** ACEITO — base e âncora entram na linha de base; nenhum código de produto.

### Ciclo 4 — MVP do bot (contrato v1.0)

- **Hipótese:** com cliente SGS próprio, handlers finos e erro tratado, o bot atende aos
  12 critérios do contrato sem banco e sem dependência paga.
- **Mudança:** pacote `src/bot_indicadores` (config, bcb, formatacao, handlers, app),
  suíte em `tests/` com API mockada, README classificado, `requirements.txt` fixo.
- **Métrica antes:** 6 testes. **Depois:** 38 testes passando.
- **Verificação:** `.venv\Scripts\python.exe -m pytest` verde; `main()` sem token sai com
  código 1 e mensagem clara; nenhuma chamada de rede nos testes.
- **Decisão:** ACEITO.

### Ciclo 5 — quarto comando `/poupanca` (SGS 195)

- **Hipótese:** acrescentar um indicador de rendimento fixo aumenta a utilidade sem
  aumentar complexidade, porque reusa o mesmo caminho de `/selic`.
- **Mudança:** `poupanca` em `CODIGOS`/`ROTULO`, handler `poupanca`, mensagem "% ao mês",
  registro no `CommandHandler` e no `/start`.
- **Métrica:** comandos com teste de resposta: **3 → 4**. Testes: 38 → 40.
- **Verificação:** suíte verde; `/poupanca` aparece no `/start` e responde com data.
- **Decisão:** ACEITO. Ressalva: o código 195 não pôde ser validado ao vivo (SGS
  bloqueando o IP); está documentado no README e em `NOTES.md`.

### Ciclo 6 — cache em memória de 60 s

- **Hipótese:** consultas repetidas em curto intervalo não precisam bater no BCB de novo;
  cache em memória reduz latência e risco de bloqueio sem violar "sem cache persistente".
- **Mudança:** `ttl_cache` no `ClienteSGS`, chave `(codigo, quantidade)`, `limpar_cache()`.
- **Métrica:** chamadas HTTP em duas consultas seguidas do mesmo indicador: **2 → 1**,
  comprovada por teste com sessão falsa. Testes: 40 → 43.
- **Verificação:** suíte verde; séries diferentes não compartilham entrada de cache;
  `ttl_cache=0` volta a consultar (teste de expiração).
- **Decisão:** ACEITO — baseline registrada em 43 testes pelo verificador.

Nenhum ciclo de produto executado. O primeiro só começa depois que o contrato definir o
sistema alvo e a métrica principal.
