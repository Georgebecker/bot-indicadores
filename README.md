# bot-indicadores

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)
![Status](https://img.shields.io/badge/status-rascunho-lightgrey)

Um projeto que se recusa a começar pelo código. Antes da primeira linha do bot de
indicadores existem regras escritas, proteção de segredos, ciclos documentados e
critérios de sucesso — para que a primeira funcionalidade não nasça no "achismo".

Se você já viu um projeto morrer por falta de métrica, este repositório é a resposta
que eu estou construindo para isso.

## Classificação

- **Propósito:** a definir no contrato do projeto; a base existe para receber o bot de indicadores.
- **Maturidade:** rascunho
- **O que está sendo treinado:** o processo de Loop Engineering (hipótese → mudança pequena → teste → medição → decisão ACEITO/REJEITADO), ainda sem sistema alvo definido.
- **Quem usaria:** a definir no contrato.

## Metodologia Loop (o diferencial)

Este projeto nasce do repositório base [`projeto_loop`](https://github.com/Georgebecker/projeto_loop)
e é construído com **Loop Engineering**: hipótese → mudança pequena → teste → medição →
decisão ACEITO/REJEITADO. Cada ciclo é registrado em [`log_loop.md`](log_loop.md) e cada
decisão não trivial em [`NOTES.md`](NOTES.md).

O loop não é discurso: [`meu-loop-agente/`](meu-loop-agente/) traz o contrato
([`program.md`](meu-loop-agente/program.md)), a configuração de máquina
([`config_loop.json`](meu-loop-agente/config_loop.json)), a linha de base
([`baseline.json`](meu-loop-agente/baseline.json)) e o verificador
([`verificar_iteracao.py`](meu-loop-agente/verificar_iteracao.py)). A linha de base atual
é **6 testes passando** (`python -m pytest`).

Este projeto não foi feito no "achismo". Cada decisão foi medida e testada — e, quando
não dá para medir ainda, eu escrevo isso na cara dura.

## O que tem aqui

Hoje o repositório é **infraestrutura, não produto**. Nada de endpoint, nada de modelo.

- [`AGENTS.md`](AGENTS.md) — regras permanentes do agente, com a âncora da base.
- [`docs/BASE_PROJETO_LOOP.md`](docs/BASE_PROJETO_LOOP.md) — o que veio da base, o que
  difere de propósito e como re-sincronizar.
- [`docs/REGRAS_DE_OURO.md`](docs/REGRAS_DE_OURO.md) — o contrato de qualidade
  (postura, processo, técnica e a Parte IV sobre Loop Engineering).
- [`meu-loop-agente/`](meu-loop-agente/) — contrato, métrica, linha de base, log e
  verificador do loop; já roda com `python -m pytest` como métrica provisória.
- [`scripts/conferir_base.py`](scripts/conferir_base.py) — confere em segundos se a base
  continua presente, idêntica e segura (ganchos ativos, `.env` ignorado, sem valor de chave).
- [`tests/test_base_projeto_loop.py`](tests/test_base_projeto_loop.py) — transforma essa
  conferência em teste: se a base se perder, a suíte fica vermelha.
- Hooks de `pre-commit` e `pre-push` que bloqueiam `.env` e valores de chave.
- Template de configuração sem segredos (`.env.example`) e `.env` apenas local.

```
bot-indicadores/
├── src/                     # código da aplicação (a definir no contrato)
├── tests/                   # testes automatizados
├── data/
│   ├── raw/                 # dados brutos (nunca alterar)
│   ├── processed/           # dados tratados
│   └── descartados/         # fora de circulação
├── docs/                    # regras de ouro e base do projeto
├── meu-loop-agente/         # contrato, métrica, verificador e log do loop
├── notebooks/               # análises exploratórias
├── scripts/                 # conferência da base
├── .githooks/               # bloqueiam .env e segredos no commit/push
├── .github/                 # agente, instruções e prompt de README
├── .env / .env.example      # configuração local sem valores de chave
├── AGENTS.md                # regras do agente e da metodologia
├── NOTES.md                 # decisões e pendências
├── log_loop.md              # ciclos de melhoria
└── LICENSE                  # MIT
```

## Como rodar

Ainda não há aplicação para executar; a base se verifica sozinha:

```powershell
git config core.hooksPath .githooks   # proteção de segredos (uma vez por clone)
pip install -r requirements.txt       # pytest fixado em versão exata
python -m pytest                      # suíte atual: 6 testes
python scripts/conferir_base.py       # a base projeto_loop continua no lugar?
python meu-loop-agente/verificar_iteracao.py estado
```

Requisitos: **Git**, **Python 3.11+** (testado em 3.14.6 nesta máquina). Nenhuma chave de
API é necessária nesta etapa: a chave vive na variável de ambiente do usuário do Windows,
nunca em arquivo.

## 🚀 Convite à interação

Este repositório é meu laboratório aberto, e ele fica bem melhor com gente dentro.

**Se você está começando:** quer fazer seu primeiro Pull Request? Eu deixei (e vou
deixar cada vez mais) tarefas fáceis com a tag `good first issue`: melhorar uma mensagem
de erro, escrever um teste simples, ajustar esta documentação. Não tenha medo de errar —
eu reviso, comento e ajudo.

**Se você já programa:** viu um gargalo, uma brecha de segurança ou um jeito melhor de
estruturar os dados? Abre uma Issue ou manda o PR. Eu quero muito trocar ideia sobre
arquitetura de dados e automação com IA.

**Se você é recrutador ou só caiu aqui de paraquedas:** este é um projeto real, não um
tutorial copiado. O jeito como eu penso está nas regras ([`AGENTS.md`](AGENTS.md)), nos
ciclos ([`log_loop.md`](log_loop.md)) e nas decisões ([`NOTES.md`](NOTES.md)). Explora
à vontade.

## Transparência e limitações

- **Sem contrato, sem código de produto.** O prompt do projeto ainda não chegou; `src/`
  segue vazio e a métrica do loop é provisória ("testes que passam").
- **A suíte cobre a base, não o bot.** São 6 testes de infraestrutura: âncora da base,
  ganchos, `.env` sem chave. Ainda não existe o teste que valida a seção
  `## Classificação` exigido pelo `AGENTS.md`.
- **Sem `.venv` criado.** O `pytest.ini` existe e o pytest roda no Python global desta
  máquina; o ambiente virtual ainda não foi montado.
- **Dependência da base local.** `scripts/conferir_base.py` espera o clone em
  `D:\Projetos\projeto_loop` (ou `PROJETO_LOOP_PATH`); sem ele, o teste fica vermelho
  de propósito.
- **Nada de produção.** Isto é uma base local, não um serviço publicado.

## Tags

```text
python
loop-engineering
data-quality
automation
indicadores
```

## Licença

MIT — veja [`LICENSE`](LICENSE).
