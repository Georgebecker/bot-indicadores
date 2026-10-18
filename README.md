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

Este projeto nasce do repositório base `projeto_loop` e é construído com
**Loop Engineering**: hipótese → mudança pequena → teste → medição → decisão
ACEITO/REJEITADO. Cada ciclo é registrado em [`log_loop.md`](log_loop.md) e cada
decisão não trivial em [`NOTES.md`](NOTES.md).

Este projeto não foi feito no "achismo". Cada decisão foi medida e testada — e, quando
não dá para medir ainda, eu escrevo isso na cara dura.

## O que tem aqui

Hoje o repositório é **infraestrutura, não produto**. Nada de endpoint, nada de modelo.

- Regras permanentes do agente e da metodologia em [`AGENTS.md`](AGENTS.md).
- Hooks de `pre-commit` e `pre-push` que bloqueiam `.env` e valores de chave.
- Template de configuração sem segredos (`.env.example`) e `.env` apenas local.
- Referência de qualidade em [`docs/REGRAS_DE_OURO.md`](docs/REGRAS_DE_OURO.md).

```
bot-indicadores/
├── src/                     # código da aplicação (a definir)
├── tests/                   # testes automatizados (a definir)
├── data/
│   ├── raw/                 # dados brutos (nunca alterar)
│   ├── processed/           # dados tratados
│   └── descartados/         # fora de circulação
├── docs/                    # regras e documentação
├── notebooks/               # análises exploratórias
├── .githooks/               # bloqueiam .env e segredos no commit/push
├── .github/                 # agente, instruções e prompt de README
├── .env / .env.example      # configuração local sem valores de chave
├── AGENTS.md                # regras do agente e da metodologia
├── NOTES.md                 # decisões e pendências
├── log_loop.md              # ciclos de melhoria
└── LICENSE                  # MIT
```

## Como rodar

Ainda não há aplicação para executar. Para trabalhar na base:

```powershell
git config core.hooksPath .githooks   # ativa a proteção de segredos
```

Requisitos: **Git** e **Python 3.11+** (a versão final será fixada no contrato).
Nenhuma chave de API é necessária nesta etapa.

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

- **Sem contrato, sem código.** O prompt do projeto ainda não chegou; por isso não há
  funcionalidade, dependência, banco ou teste.
- **Sem suíte automatizada ainda.** O `tests/` está vazio; o teste que valida a seção
  `## Classificação` é a primeira pendência técnica.
- **Sem `.venv` criado.** O `pytest.ini` existe, mas o ambiente local ainda não foi montado.
- **Python 3.11+ é provisório.** A versão exata só será fixada quando a stack for escolhida.
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
