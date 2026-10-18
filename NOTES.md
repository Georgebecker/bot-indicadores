# NOTES — bot-indicadores

Registro das decisões não triviais do projeto. Ideias fora do escopo ficam na seção
de ideias futuras e não são implementadas antes do contrato.

## Estado da base

- **2026-10-18:** base criada; aguardando o prompt/contrato do projeto.
- Nenhuma funcionalidade, stack ou banco de dados foi definido ainda; a única dependência
  é `pytest==9.1.1`, para os testes da infraestrutura.
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
- **2026-10-18:** `README.md` reescrito no padrão George Becker (gancho, badges, convite
  à interação, limitações honestas, topics) mantendo a seção `## Classificação` e sem
  declarar funcionalidade inexistente. Criado também `.github/prompts/readme.prompt.md`
  (comando `/readme`) que reaproveita a instrução em vez de duplicá-la.
- **2026-10-18:** `AGENTS.md` apareceu vazio no working tree (4 bytes) e foi restaurado
  do `HEAD` com `git restore -- AGENTS.md`; nenhum commit tinha sido feito com o arquivo
  vazio. A âncora da base agora fica no topo dele, para o arquivo não voltar a ficar órfão.

## Decisões

- **2026-10-18 — base `projeto_loop` como origem (não inspiração).** O projeto passou a
  ser sincronizado com o modelo local (`D:\Projetos\projeto_loop`, commit
  `8830840ab9644f1f4f19c104ae9d6396bf0a5d52`). Foram trazidos: `.gitattributes`,
  `requirements.txt` e `meu-loop-agente/` completo (contrato, config de máquina,
  `system_prompt`, `log.md`, `baseline.json`, `outputs/`, `workspace/` e verificador).
  Divergências conscientes (`config_loop.json`, `program.md`, `system_prompt.md`,
  `workspace/` sem os exemplos Next.js) e arquivos **não** copiados
  (`scripts/criar_projeto_base.ps1`, `docs/GUIA_NOVO_PROJETO.md`) estão justificados em
  [`docs/BASE_PROJETO_LOOP.md`](docs/BASE_PROJETO_LOOP.md).
- **2026-10-18 — âncora contra esquecimento.** A base virou checagem executável:
  `scripts/conferir_base.py` (arquivos do modelo, hash das Regras de Ouro e dos ganchos,
  `core.hooksPath`, `.env` ignorado, nenhum valor de chave) e
  `tests/test_base_projeto_loop.py` (vermelho se a âncora se perder). `AGENTS.md` e
  `.github/copilot-instructions.md` apontam para ela.
- **2026-10-18 — dependência `pytest==9.1.1`.** Justificativa: o `AGENTS.md` exige teste
  automatizado (inclusive da classificação) e o verificador do loop mede testes que
  passam. Versão exata fixada conforme a regra de fixar versões. Nenhuma outra
  dependência foi adicionada.
- **2026-10-18 — métrica provisória do loop.** `meu-loop-agente/config_loop.json` mede
  "testes que passam" (`maior_melhor`) com `python -m pytest` (sem `-q` duplicado, porque
  o `pytest.ini` já aplica `-q` e o resumo "N passed" desaparecia). Linha de base
  gravada em 6 testes. Será substituída quando o contrato definir a métrica do produto.
  Observação de método: a linha de base foi gravada **depois** do Ciclo 3, então o
  verificador sugere REJEITADO para essa mudança (6 → 6); o ciclo está julgado em
  `log_loop.md` com a medição real do antes (0 testes) e do depois (6 testes).
- **2026-10-18 — valor de chave saiu do `.env`.** O conferidor achou
  `DEEPSEEK_API_KEY` com valor no `.env` (35 caracteres). Migrado com
  `segredos.ps1 -MigrarArquivos`: como já existia um `DEEPSEEK_API_KEY` diferente no
  ambiente do usuário, o valor antigo do arquivo foi guardado como
  `DEEPSEEK_API_KEY_BOT_INDICADORES` e a linha ficou comentada. **Pendência do dono:**
  decidir qual valor deve valer como `DEEPSEEK_API_KEY` (definir pelo `segredos.ps1`).

- **2026-10-18 — capturas de tela como regra (máximo 5 por projeto).** Projeto com
  interface gráfica passa a documentar o que o usuário vê: até 5 prints em `docs/img/`,
  com alt text e legenda no README, capturados só depois da suíte verde e nunca com
  token, ID de chat ou dado pessoal. A regra vive em instrução global
  (`%USERPROFILE%\.copilot\instructions\capturas-de-tela.instructions.md`) e foi
  amarrada no `AGENTS.md`. Neste projeto a interface é a conversa do bot no Telegram;
  se não houver como capturar (sem token/ambiente), a pendência é registrada, jamais
  simulada.

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
- Substituir o objetivo provisório de `meu-loop-agente/program.md` e a métrica
  "testes que passam" quando o contrato chegar.
- Criar o teste que valida a seção `## Classificação` do `README.md` (exigido pelo
  `AGENTS.md`).
- Decidir qual valor deve valer como `DEEPSEEK_API_KEY` no ambiente do usuário
  (`DEEPSEEK_API_KEY_BOT_INDICADORES` guarda o que estava no `.env`).
