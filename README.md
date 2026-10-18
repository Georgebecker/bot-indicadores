# bot-indicadores

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)
![Status](https://img.shields.io/badge/status-us%C3%A1vel-brightgreen)

Um bot de Telegram que responde **dólar PTAX, Selic meta e IPCA acumulado em 12 meses**
direto do Banco Central — sem abrir site, sem caçar planilha, sem depender de portal
lento. Você digita `/dolar` no celular e recebe o número com a data de referência.

É um projeto de estudo com cara de utilidade: bot pequeno, assíncrono, com erro tratado
de verdade e cada decisão registrada.

## Classificação

- **Propósito:** consultar indicadores econômicos brasileiros (dólar PTAX, Selic meta e IPCA) dentro do Telegram, com data de referência e sem depender de banco de dados.
- **Maturidade:** `usável`
- **O que está sendo treinado:** assincronismo com `python-telegram-bot`, integração com API externa em contexto de bot e tratamento de erro em canal conversacional.
- **Quem usaria:** quem acompanha câmbio, juros e inflação no dia a dia e quer o número em segundos no celular, além de quem estuda bots em Python.

## Metodologia Loop (o diferencial)

Este projeto nasce do repositório base [`projeto_loop`](https://github.com/Georgebecker/projeto_loop)
e é construído com **Loop Engineering**: hipótese → mudança pequena → teste → medição →
decisão ACEITO/REJEITADO. Cada ciclo está em [`log_loop.md`](log_loop.md) e cada decisão
não trivial em [`NOTES.md`](NOTES.md).

O loop não é discurso: [`meu-loop-agente/`](meu-loop-agente/) tem o contrato
([`program.md`](meu-loop-agente/program.md)), a configuração de máquina
([`config_loop.json`](meu-loop-agente/config_loop.json)), a linha de base
([`baseline.json`](meu-loop-agente/baseline.json)) e o verificador
([`verificar_iteracao.py`](meu-loop-agente/verificar_iteracao.py)).

Este projeto não foi feito no "achismo". Cada decisão foi medida e testada.

## Comandos

```text
/start     boas-vindas com a lista de comandos
/dolar     cotação PTAX de venda do dólar + data de referência   (SGS 1)
/selic     taxa Selic meta + data de referência                  (SGS 432)
/ipca      IPCA acumulado em 12 meses + último mês               (SGS 433)
/poupanca  rendimento da poupança + data de referência           (SGS 195)
```

Exemplo de resposta:

```text
Dólar PTAX (venda): R$ 5,2079
Referência: 01/10/2026
Fonte: Banco Central (SGS 1)
```

## O que tem aqui
- [`src/bot_indicadores/bcb.py`](src/bot_indicadores/bcb.py) — cliente assíncrono da API SGS: timeout curto, poucas tentativas, `requests` fora do event loop, resposta não-JSON tratada como falha e cache em memória de 60 s (por indicador).
- [`src/bot_indicadores/handlers.py`](src/bot_indicadores/handlers.py) — os quatro comandos e a mensagem amigável de erro.
- [`src/bot_indicadores/config.py`](src/bot_indicadores/config.py) — token só de variável de ambiente, com falha clara antes de conectar.
- [`src/bot_indicadores/app.py`](src/bot_indicadores/app.py) — montagem da `Application` e polling.
- [`tests/`](tests/) — suíte com API mockada (nenhuma chamada de rede no teste) e o teste da classificação.
- [`scripts/conferir_base.py`](scripts/conferir_base.py) — confere a base `projeto_loop` em segundos.
- [`docs/REGRAS_DE_OURO.md`](docs/REGRAS_DE_OURO.md) — contrato de qualidade do projeto; a **Parte V** trata da didática obrigatória.
- [`docs/COMO_LER_O_CODIGO.md`](docs/COMO_LER_O_CODIGO.md) — guia para iniciantes: o que é API, JSON, assíncrono, cache e mock, com analogias.
- [`meu-loop-agente/`](meu-loop-agente/) — o loop operacional.

```
bot-indicadores/
├── src/bot_indicadores/     # config, bcb, formatacao, handlers, app
├── tests/                   # pytest (API mockada)
├── docs/                    # regras de ouro e base do projeto
├── meu-loop-agente/         # contrato, métrica e verificador do loop
├── scripts/                 # conferência da base
├── .githooks/               # bloqueiam .env e segredos no commit/push
├── .github/                 # instruções e prompt de README
├── requirements.txt         # versões exatas
└── log_loop.md / NOTES.md   # ciclos e decisões
```

## Como rodar

Requisitos: **Python 3.11+** (testado em 3.14.6) e **Git**. Nada de banco, nada pago.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# o token NUNCA vai para arquivo: fica na variável de ambiente do usuário
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\scripts\segredos.ps1" -Definir TELEGRAM_BOT_TOKEN

# reabra o terminal para enxergar a variável e rode
$env:PYTHONPATH = "src"
python -m bot_indicadores
```

Sem token, o bot não sobe e explica o motivo (não tenta conectar). Testes:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## 🚀 Convite à interação

Este repositório é meu laboratório aberto, e fica melhor com gente dentro.

**Se você está começando:** quer fazer seu primeiro Pull Request? Tem tarefa com a tag
`good first issue` esperando: melhorar uma mensagem de erro, escrever um teste novo,
ajustar este README. Não tenha medo de errar — eu reviso e ajudo. E se um comentário
não te ensinou nada, isso é bug: abre uma issue contando onde travou
([guia de leitura](docs/COMO_LER_O_CODIGO.md)).

**Se você já programa:** viu gargalo no cliente do BCB, uma brecha ou um jeito melhor de
estruturar os handlers? Abre uma Issue ou manda o PR. Adoro trocar ideia sobre
assincronismo, arquitetura de dados e automação com IA.

**Se você é recrutador ou caiu aqui de paraquedas:** este é um projeto real, não tutorial
copiado. O jeito como eu penso está nas regras ([`AGENTS.md`](AGENTS.md)), nos ciclos
([`log_loop.md`](log_loop.md)) e nas decisões ([`NOTES.md`](NOTES.md)).

## Transparência e limitações

- **API do BCB instável.** A SGS respondeu erro interno e depois uma página XML
  "Requisição inválida!" durante o desenvolvimento — o bot trata como falha e avisa o
  usuário, mas a disponibilidade não está sob meu controle.
- **Sem verificação ao vivo nesta máquina.** O ambiente não tem `TELEGRAM_BOT_TOKEN`
  definido, então o fluxo real no Telegram não foi exercitado aqui; o comportamento é
  coberto por testes com API e Telegram mockados. Com o token definido, o bot roda com
  `python -m bot_indicadores`.
- **IPCA é acumulado por composição** dos últimos 12 valores mensais (não é o número
  oficial de "12 meses" do IBGE, que usa a série completa).
- **Polling, não webhook.** Simples para rodar local; não escala para muitas instâncias.
- **Cache só em memória, com TTL de 60 s.** É o que evita bater no BCB a cada mensagem,
  mas reinicia do zero quando o bot reinicia (cache persistente é proibido por contrato).
- **Sem banco, sem autenticação de usuário** — por contrato.
- **Capturas de tela pendentes** (regra de até 5 por projeto): ainda sem `TELEGRAM_BOT_TOKEN`
  e com a API do BCB em erro, uma imagem mostraria só a mensagem de erro. Preferi não
  publicar print parcial nem recriar a tela — a pendência está em [`NOTES.md`](NOTES.md).

## Tags

```text
python
telegram-bot
bcb
indicadores
asyncio
loop-engineering
```

## Licença

MIT — veja [`LICENSE`](LICENSE).
