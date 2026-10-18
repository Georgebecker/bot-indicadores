# AGENTS.md — bot-indicadores

Regras permanentes do agente neste projeto. Leia antes de qualquer alteração.

## Base de trabalho: `projeto_loop` (ler antes de tudo)

Todo projeto nasce do modelo [`projeto_loop`](https://github.com/Georgebecker/projeto_loop),
que está clonado nesta máquina em `D:\Projetos\projeto_loop` (commit de referência
`8830840ab9644f1f4f19c104ae9d6396bf0a5d52`). Não é inspiração: é a origem do método.

Antes de planejar qualquer mudança, rode:

```powershell
python scripts/conferir_base.py
```

- O que veio da base, o que difere e como re-sincronizar: seção 9 de `MEMORIA.md`
  (local, fora do upload — histórico não é produto).
- Contrato de qualidade (postura, processo, técnica, Loop Engineering): [`docs/REGRAS_DE_OURO.md`](docs/REGRAS_DE_OURO.md).
- Loop operacional (contrato e métrica): [`meu-loop-agente/program.md`](meu-loop-agente/program.md). O verificador da base não é versionado aqui — a métrica é lida direto do `pytest`.
- `tests/test_base_projeto_loop.py` fica vermelho se a base sumir ou divergir.
- Em conflito entre este arquivo e a base, **este arquivo vence**; registre o motivo em
  `MEMORIA.md`.

## Estado

Base criada em **2026-10-18**. O contrato/prompt do projeto ainda não foi recebido.
**Não implemente funcionalidades antes do contrato.**

## Idioma

Português do Brasil em respostas, commits, logs, comentários, documentação e mensagens
de erro. Identificadores de código em inglês. Termos técnicos consagrados podem ficar
como estão.

## Modelo / sessão

- O modelo pode mudar a cada sessão; confira o ativo com:
  `powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\modelo-ativo.ps1" -Pasta (Get-Location).Path`
- Prefira passos curtos e direcionados; evite despejar arquivos grandes no contexto.

## Segredos e `.env`

- **Nenhum arquivo versionado guarda valor de chave.** Nem `DEEPSEEK_API_KEY`, nem
  `OPENAI_API_KEY`, nem token, senha, DSN ou chave privada.
- **O `.env` é local e PODE guardar o valor da chave** — é o único lugar previsto para
  isso. O que não pode, em nenhuma circunstância, é ele subir: `.env` nunca vai para o
  git, para o GitHub, para print ou para resposta. O `.env.example` é o modelo
  versionado, sem valores.
- **Nunca altere, comente, migre ou apague o conteúdo do `.env` por conta própria.**
  Ele pertence ao dono. `segredos.ps1 -MigrarArquivos` só roda se o dono pedir.
- A variável de ambiente do usuário do Windows é o caminho **preferido** para o valor
  (sobrevive a apagar o projeto), mas não é obrigatório: `.env` preenchido é válido.
  Comandos, quando o dono pedir:

```powershell
# listar nomes (nunca valores)
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\segredos.ps1" -Listar

# definir uma chave (o valor não aparece na tela)
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\segredos.ps1" -Definir NOME_DA_CHAVE
```

- Nunca imprimir valor de chave em resposta, log, commit ou saída de comando.
- Nunca usar `git add -f` em arquivo de segredo. Se um `.env` entrar no índice:
  `git rm --cached .env`.
- O que a automação verifica é só a fronteira: `.env` ignorado, fora do índice e
  nenhum valor de chave em arquivo versionado. O conteúdo do `.env` não é auditado.

## Capturas de tela (interface gráfica)

- Projeto com interface gráfica (web, desktop, painel, notebook ou conversa de bot):
  no máximo **5 capturas por projeto**, salvas em `docs/img/` com nome em kebab-case.
- Cada imagem entra no README com alt text e legenda explicando o que acontece; a
  captura é evidência, não enfeite.
- Nunca aparece token, chave, ID de chat, nome de terceiro ou caminho com usuário.
- Capturar só depois da suíte verde; se o ambiente não permitir, registrar a pendência
  em `MEMORIA.md` em vez de recriar a tela.

## Didática obrigatória

- Todo `.py` começa dizendo **o que é o arquivo e para que serve**, sem jargão.
- Toda função tem docstring curta: o que entra, o que sai e **por que existe**.
- Antes de trecho difícil, explique com **analogia do dia a dia** (fila, bilhete,
  caderno de recados). Comente o **motivo**, nunca o óbvio (`# soma 1` não ensina).
- Mensagem de erro é aula: o que aconteceu, por que e o que fazer agora — em
  português, sem jargão e sem stack trace para o usuário final.
- Nomes de variáveis também ensinam: `pontos_da_serie`, não `p`; `mensagem_de_erro`, não `m`.
- Teste prático: alguém que nunca viu o projeto precisa conseguir explicar o módulo
  só lendo os comentários. Se não conseguir, o arquivo não está pronto.
- Comentário que mente é pior que comentário nenhum: mudou o código, mude o
  comentário na mesma alteração.
- Regra completa: `docs/REGRAS_DE_OURO.md`, **Parte V — Didática obrigatória**.
- Limite: didático não é verboso; o alvo é clareza, não quantidade de `#`.

## Metodologia: Loop Engineering

- Uma mudança pequena por ciclo: **hipótese → mudança → teste → métrica → decisão**.
- Decisão **ACEITO** mantém e atualiza a linha de base; **REJEITADO** reverte.
- Registrar cada decisão não trivial e cada ciclo em `MEMORIA.md` — **um arquivo
  local**, fora do upload (histórico não é produto). Não criar `NOTES.md` nem
  `log_loop.md`: eram dois arquivos dizendo o mesmo.
- Regras da **Parte VII** das Regras de Ouro estão **desativadas**: não use nenhuma
  delas para justificar mudança sem antes ativá-la pelo caminho descrito lá.
- O `README.md` deve ter a seção `## Classificação` com quatro campos preenchidos:
  Propósito, Maturidade, O que está sendo treinado, Quem usaria.
- A maturidade declarada deve refletir o estado real; se houver testes verdes, README
  completo e publicação, pode ser `usável`; caso contrário, `funcional` ou `rascunho`.
- Incluir teste automatizado que verifique a presença e a validade da classificação.
- Não adicionar dependências sem justificativa em `MEMORIA.md`; fixar versões exatas.
- `pytest.ini` com `pythonpath = .`.
- Ler e escrever arquivos sempre com `encoding="utf-8"`.
- Não declarar pronto sem rodar o checklist de critérios de sucesso item por item.

## Ambiente

- Windows, PowerShell 5.1: não usar `&&`, `||`, `??`; use `;` e `if ($?)`.
- Python no `.venv` local; nunca versionar `.venv`.
- Git hooks em `.githooks`; ativar com `git config core.hooksPath .githooks`.
- Entregar relatório estruturado, não resumo informal.

## Próximo passo

Aguardar o prompt do usuário. Quando ele chegar, transformar o contrato em critérios
de sucesso verificáveis antes de escrever código, e substituir o objetivo provisório de
`meu-loop-agente/program.md`.
