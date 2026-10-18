# bot-indicadores

Base inicial do projeto `bot-indicadores`, criada em **2026-10-18**. O contrato/prompt
do projeto ainda não foi recebido; nenhuma funcionalidade foi implementada.

## Classificação

- **Propósito:** a definir no contrato do projeto; a base existe para receber o bot de indicadores.
- **Maturidade:** rascunho
- **O que está sendo treinado:** o processo de Loop Engineering (hipótese → mudança pequena → teste → medição → decisão ACEITO/REJEITADO), ainda sem sistema alvo definido.
- **Quem usaria:** a definir no contrato.

## Estado atual

- Estrutura de pastas, `.env`, `.env.example`, `.gitignore`, hooks de proteção e licença.
- Sem dependências, sem código de aplicação, sem testes e sem banco de dados.
- Próximo passo: receber o prompt/contrato e registrar as decisões em [`NOTES.md`](NOTES.md).

## Estrutura

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
├── .env / .env.example      # configuração local sem valores de chave
├── AGENTS.md                # regras do agente e da metodologia
├── NOTES.md                 # decisões e pendências
├── log_loop.md              # ciclos de melhoria
└── LICENSE                  # MIT
```

## Ambiente

- **Python 3.11+** (a confirmar conforme a stack escolhida no contrato).
- **Git** com os hooks ativos: `git config core.hooksPath .githooks`.
- Nenhuma chave ou segredo é necessária nesta base.

## Como o agente deve trabalhar

As regras completas estão em [`AGENTS.md`](AGENTS.md). Em resumo: português do Brasil,
segredos somente em variável de ambiente, mudanças pequenas com teste e métrica,
decisões registradas em `NOTES.md` e ciclos em `log_loop.md`.

## Licença

MIT — veja [`LICENSE`](LICENSE).
