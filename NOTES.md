# NOTES — bot-indicadores

Registro das decisões não triviais do projeto. Ideias fora do escopo ficam na seção
de ideias futuras e não são implementadas antes do contrato.

## Estado da base

- **2026-10-18:** base criada; aguardando o prompt/contrato do projeto.
- Nenhuma funcionalidade, stack, dependência ou banco de dados foi definido ainda.
- `.env` e `.env.example` criados pelo template global, sem valor de chave.
- `.gitignore` protege `.env`, `.env.*`, ambientes virtuais, caches e dados.
- Hooks de `commit` e `push` copiados da base do Loop Engineering.
- `docs/REGRAS_DE_OURO.md` copiado como referência de qualidade.
- A licença é MIT.
- **2026-10-18:** criado `.github/agents/deepseek-flash.agent.md` como persona de
  desenvolvimento do projeto (modelo `deepseek/deepseek-v4-flash`, esforço alto). O
  agente carrega as regras de `AGENTS.md` e exige contrato antes de qualquer código;
  não é funcionalidade do produto.
- **2026-10-18:** adicionado `.github/instructions/readme-george-becker.instructions.md`
  (`applyTo: "**/README.md"`) com o padrão George Becker de README interativo. É
  instrução de arquivo: só entra no contexto quando o README é editado, portanto não
  consome contexto nas demais tarefas nem altera o Loop Engineering. Em conflito,
  `AGENTS.md` prevalece e a seção `## Classificação` continua obrigatória.
- **2026-10-18:** `AGENTS.md` apareceu vazio no working tree (4 bytes) e foi restaurado
  do `HEAD` com `git restore -- AGENTS.md`; nenhum commit tinha sido feito com o arquivo
  vazio.
- **2026-10-18:** `README.md` reescrito no padrão George Becker (gancho, badges, convite
  à interação, limitações honestas, topics) mantendo a seção `## Classificação` e sem
  declarar funcionalidade inexistente. Criado também `.github/prompts/readme.prompt.md`
  (comando `/readme`) que reaproveita a instrução em vez de duplicá-la.

## Decisões pendentes (dependem do prompt)

- Stack e versões.
- Fonte dos indicadores e formato dos dados.
- Métrica principal do loop.
- Estratégia de testes e de execução.
- Se haverá banco, API, frontend ou apenas script.

## Ideias futuras (não implementadas)

- A definir no contrato.

## Pendências

- Receber o novo prompt e transformar o contrato em critérios de sucesso verificáveis.
- Ativar os hooks no clone/repositório: `git config core.hooksPath .githooks`.
