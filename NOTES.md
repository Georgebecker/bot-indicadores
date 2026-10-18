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

## Contrato v1.0 recebido (2026-10-18)

Contrato de especificação do projeto recebido e transformado em critérios verificáveis.
Objetivo: bot de Telegram com `/start`, `/dolar`, `/selic` e `/ipca` usando a API SGS do
BCB, sem banco, sem webhook, sem dependência paga e sem token em arquivo.

### Pesquisa e escolhas conscientes

- **python-telegram-bot 22.8** (contrato pede v20+, versão exata fixada). Não usei
  template FastAPI: o escopo é polling, não webhook. Os handlers seguem o padrão mínimo
  da própria biblioteca (`Application`, `CommandHandler`, handler `async`), sem copiar
  código de exemplo externo.
- **`bacendata` não foi usada.** Seria mais uma dependência para resolver algo que uma
  chamada `requests` já resolve; o contrato permite as duas abordagens e exige registrar
  a escolha. Cliente próprio também deixa o tratamento de erro explícito (página XML de
  erro do BCB, `{"erro": ...}`, lista vazia, item malformado).
- **Polling em vez de webhook**, como manda o contrato: roda local sem expor porta.
- **Restrição por lista de usuários não foi implementada** (fora do MVP): anotada em
  "Ideias futuras".

### Decisões de comportamento

- `/dolar` → **PTAX de venda** (SGS 1), com data de referência — é o número usado como
  referência de mercado.
- `/selic` → **Selic meta** (SGS 432), último valor disponível.
- `/ipca` → **acumulado em 12 meses por composição** dos últimos 12 valores mensais
  (SGS 433) + o valor do último mês. Não é o número oficial do IBGE; está no README
  como limitação.
- `/poupanca` → SGS 195, "% ao mês" (aceito no Ciclo 2 do loop).
- Erro de API: timeout de 8 s, 2 tentativas com 1 s de espera, resposta não-JSON tratada
  como falha e mensagem amigável no chat, sem stack trace.
- `requests` roda em `asyncio.to_thread` para não bloquear o event loop.
- Cache de 60 s **apenas em memória** (Ciclo 3): reduz chamadas ao BCB sem violar a
  proibição de cache persistente.
- Token: só de `TELEGRAM_BOT_TOKEN` no ambiente; `obter_token` falha antes de qualquer
  conexão e nunca imprime o valor.

### Dependências (justificativa exigida pelo AGENTS.md)

| Dependência | Versão | Por quê |
|---|---|---|
| `python-telegram-bot` | 22.8 | Interface do Telegram exigida pelo contrato (v20+), polling assíncrono. |
| `requests` | 2.34.2 | Cliente HTTP síncrono, simples e explícito para a SGS. |
| `pytest` | 9.1.1 | Suíte automatizada exigida pelo contrato e pelo AGENTS.md. |
| `pytest-asyncio` | 1.4.0 | Testar handlers e cliente assíncronos sem subir o bot. |

`pytest.ini` passou a usar `pythonpath = . src` (além do `.` exigido) para importar o
pacote que vive em `src/`.

### Bloqueios encontrados

- **API SGS instável neste ambiente.** A primeira chamada devolveu
  `{"erro":{"statusCode":500,"detail":"Internal error"}}`; depois, todas as séries
  testadas (1, 11, 432, 433, 195, 4389, 4390) passaram a devolver uma página XML
  "Requisição inválida!" com HTTP 200 — comportamento de bloqueio/limite do serviço.
  A API Olinda do mesmo BCB respondeu normalmente, provando que a rede funciona. Por isso
  o cliente trata resposta não-JSON como falha e a verificação ao vivo ficou pendente.
- **Sem `TELEGRAM_BOT_TOKEN` no ambiente desta máquina.** O bot foi validado por teste
  (montagem da `Application`, handlers com Telegram mockado, falha de token), mas não
  conversou com o Telegram de verdade. Consequência: as capturas de tela (regra de até 5
  por projeto) ficam pendentes.
- **`python` global não tem as dependências do bot**; o verificador do loop passou a usar
  `.venv\Scripts\python.exe -m pytest` para medir o ambiente real.

- **2026-10-18 — classificação final `usável`.** Reavaliação após o push: suíte verde
  (43 testes), README completo e repositório privado publicado. O critério do contrato
  está satisfeito; se algum dos três cair, a maturidade volta para `funcional`.

## Repositório público (2026-10-18 19:12)

O repositório passou de privado para **público** para permitir colaboração (o contrato
previa privado; esta é a primeira divergência consciente em relação a ele, registrada
aqui). Auditoria feita antes da mudança, commit por commit:

- `.env` nunca entrou no histórico; nenhum padrão de token/chave versionado.
- Nenhum caminho `C:\Users\...` no repositório.
- Único dado pessoal: a chave PIX em `docs/REGRAS_DE_OURO.md`, herdada da base
  `projeto_loop`, que já é pública — portanto não houve exposição nova.
- O token continua exclusivamente em variável de ambiente do usuário.

Arquivos versionados: 50, todos necessários ao produto, ao método ou à segurança
(ganchos). Nada de artefato de execução: `meu-loop-agente/outputs/*` e `.venv/` estão
ignorados.

## Ideias futuras (não implementadas)

- Botões inline para escolher o indicador (o contrato cita como candidato; ficou fora dos
  dois ciclos executados).
- `/cdi` ou `/poupanca` com `bacendata` e cache em disco.
- Restrição de comandos por lista de IDs autorizados.
- Webhook com FastAPI para deploy em produção.
- Alerta automático quando um indicador cruzar um limite definido pelo usuário.

## Pendências

- Receber o novo prompt e transformar o contrato em critérios de sucesso verificáveis.
- Substituir o objetivo provisório de `meu-loop-agente/program.md` e a métrica
  "testes que passam" quando o contrato chegar.
- Criar o teste que valida a seção `## Classificação` do `README.md` (exigido pelo
  `AGENTS.md`).
- Decidir qual valor deve valer como `DEEPSEEK_API_KEY` no ambiente do usuário
  (`DEEPSEEK_API_KEY_BOT_INDICADORES` guarda o que estava no `.env`).
- Definir `TELEGRAM_BOT_TOKEN` com o `segredos.ps1` para validar o bot ao vivo e tirar as
  capturas de tela (máximo 5) da conversa. Comando de validação, depois de definir e
  reabrir o terminal:

  ```powershell
  cd D:\Projetos\bot-indicadores
  $env:PYTHONPATH = "src"
  .\.venv\Scripts\python.exe -m bot_indicadores
  ```

  No Telegram: `/start`, `/dolar`, `/selic`, `/ipca`, `/poupanca`.
- Revalidar as séries 1, 432, 433 e 195 quando a SGS liberar o acesso deste IP. Testes de
  2026-10-18: às 15:27 as quatro devolviam a página XML "Requisição inválida!"; às 17:10
  voltaram a devolver `{"erro":{"statusCode":500}}`. Continua sem dado real.
- **Capturas de tela: canceladas nesta rodada por decisão do dono (2026-10-18 17:12).**
  Três bloqueios simultâneos: sem `TELEGRAM_BOT_TOKEN`; `web.telegram.org` sem sessão
  (pede QR, e o login da conta fica para depois, feito pelo próprio dono); e o
  BCB em erro 500, o que faria toda print de indicador mostrar apenas a mensagem de erro.
  Alternativas descartadas: recriar a tela do Telegram à mão (seria simular evidência) e
  servidor local imitando a Bot API (validaria a própria suposição, não o mundo real).
  Quando houver token e o BCB responder, seguir a regra global de até 5 imagens em
  `docs/img/` com legenda.

## Issues de engajamento criadas (2026-10-18)

Criadas no repositório privado com a label `good first issue`, todas apontando para
arquivos e testes que já existem:

- #1 Adicionar teste de expiração real do cache com relógio controlado
- #2 Melhorar a mensagem de erro do BCB distinguindo indisponibilidade, resposta
  inválida e série sem dados
- #3 Documentar em `docs/API.md` o contrato do cliente SGS

## Protocolo: Bot API e não MTProto (2026-10-18)

Decisão registrada porque o dono questionou o assunto: bots usam a **Bot API**
(HTTP/JSON em `api.telegram.org/bot<token>/…`), que é o que o `python-telegram-bot`
implementa. A **MTProto** (`core.telegram.org/mtproto`) é a camada binária criptografada
dos **aplicativos cliente** — a própria documentação diz que serve a "applications
running on mobile devices". Adotá-la exigiria `api_id` + `api_hash` (my.telegram.org),
uma biblioteca diferente (Telethon/Pyrogram) e um arquivo de sessão persistente, o que
contraria três proibições do contrato (sem autenticação de usuário, sem cache
persistente, token só via ambiente) sem ganho funcional para quatro comandos.
