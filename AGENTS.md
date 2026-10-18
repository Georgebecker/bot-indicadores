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

- O que veio da base, o que difere e como re-sincronizar: [`docs/BASE_PROJETO_LOOP.md`](docs/BASE_PROJETO_LOOP.md).
- Contrato de qualidade (postura, processo, técnica, Loop Engineering): [`docs/REGRAS_DE_OURO.md`](docs/REGRAS_DE_OURO.md).
- Loop operacional (contrato, métrica, verificador): [`meu-loop-agente/`](meu-loop-agente/).
- `tests/test_base_projeto_loop.py` fica vermelho se a base sumir ou divergir.
- Em conflito entre este arquivo e a base, **este arquivo vence**; registre o motivo em
  `docs/BASE_PROJETO_LOOP.md`.

## Estado

Base criada em **2026-10-18**. O contrato/prompt do projeto ainda não foi recebido.
**Não implemente funcionalidades antes do contrato.**

## Idioma

Português do Brasil em respostas, commits, logs, comentários, documentação e mensagens
de erro. Identificadores de código em inglês. Termos técnicos consagrados podem ficar
como estão.

## Modelo / sessão

- Modelo ativo nesta máquina: **deepseek/deepseek-v4-flash** (esforço de raciocínio alto).
- O modelo pode mudar; a fonte de verdade é o comando:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\modelo-ativo.ps1" -Pasta (Get-Location).Path
```

- Prefira passos curtos e direcionados; evite despejar arquivos grandes no contexto.

## Segredos e `.env`

- **Nenhum arquivo guarda valor de chave.** Nem `DEEPSEEK_API_KEY`, nem `OPENAI_API_KEY`,
  nem token, senha, DSN ou chave privada.
- O `.env` é local e nunca versionado; o `.env.example` é o modelo versionado, sem valores.
- O valor vive na variável de ambiente do usuário do Windows. Comandos:

```powershell
# listar nomes (nunca valores)
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\segredos.ps1" -Listar

# definir uma chave (o valor não aparece na tela)
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\segredos.ps1" -Definir NOME_DA_CHAVE

# auditar arquivos
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\segredos.ps1" -ConferirArquivos -Pasta "D:\Projetos"
```

- Nunca imprimir valor de chave em resposta, log, commit ou saída de comando.
- Nunca usar `git add -f` em arquivo de segredo. Se um `.env` entrar no índice:
  `git rm --cached .env`.

## Metodologia: Loop Engineering

- Uma mudança pequena por ciclo: **hipótese → mudança → teste → métrica → decisão**.
- Decisão **ACEITO** mantém e atualiza a linha de base; **REJEITADO** reverte.
- Registrar cada decisão não trivial em `NOTES.md` e cada ciclo em `log_loop.md`.
- O `README.md` deve ter a seção `## Classificação` com quatro campos preenchidos:
  Propósito, Maturidade, O que está sendo treinado, Quem usaria.
- A maturidade declarada deve refletir o estado real; se houver testes verdes, README
  completo e publicação, pode ser `usável`; caso contrário, `funcional` ou `rascunho`.
- Incluir teste automatizado que verifique a presença e a validade da classificação.
- Não adicionar dependências sem justificativa em `NOTES.md`; fixar versões exatas.
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
