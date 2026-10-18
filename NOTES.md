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
