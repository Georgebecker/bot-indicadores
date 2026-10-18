# Loop Program — bot-indicadores

> Este arquivo é o CONTRATO do agente. Só o humano altera.
> Os números ficam em `baseline.json`; comandos e medição, em `config_loop.json`.
> Mantenha os três coerentes entre si.

## OBJETIVO

Manter o bot de Telegram do projeto funcionando e confiável: responder `/start`,
`/dolar`, `/selic` e `/ipca` (e `/poupanca`, aceito no Ciclo 2) com dados da API SGS do
Banco Central, com data de referência, tratamento de falha da API sem quebrar o chat e
token exclusivamente em variável de ambiente.

## BASELINE E META

- Fonte dos números: `baseline.json` (valor inicial, melhor valor, meta).
- Métrica principal: quantidade de testes que passam (`python -m pytest`).
- Eficiência de cache é medida por teste (`tests/test_bcb.py`): duas consultas seguidas do
  mesmo indicador precisam gerar **uma** chamada HTTP.

## ARQUIVOS PERMITIDOS (o agente só mexe aqui)

- `src/**`
- `tests/**`
- `docs/**`
- `README.md`
- `NOTES.md`
- `log_loop.md`
- `requirements.txt` (com justificativa em `NOTES.md`)

## ARQUIVOS PROIBIDOS

- `.env`, `.env.example`, segredos e credenciais (qualquer valor de chave)
- `.githooks/**`
- `AGENTS.md`, `.github/**`
- `meu-loop-agente/program.md`, `meu-loop-agente/config_loop.json`,
  `meu-loop-agente/system_prompt.md`
- Qualquer caminho fora do repositório

## COMANDOS DE VERIFICAÇÃO (obrigatórios)

- Fonte de máquina: `config_loop.json` -> `verificacao.comandos`.
- Conteúdo atual: `python -m pytest`.

## MÉTRICA PRINCIPAL

- Nome: quantidade de testes que passam.
- Direção: maior é melhor.
- Comando e leitura: `config_loop.json` -> `metrica`.

## MÉTRICAS SECUNDÁRIAS (não podem piorar)

- Testes com falha ou erro: zero.
- `python scripts/conferir_base.py` continua saindo com código 0.
- Nenhuma chamada de rede nos testes (a API é sempre mockada).

## CRITÉRIO DE ACEITE

- Todos os comandos de verificação passam; E
- A métrica principal melhora (maior que o melhor valor registrado).

## CRITÉRIO DE REJEIÇÃO

- Qualquer comando falha; OU
- A métrica fica igual ou pior.

## POLÍTICA DE MUDANÇA

- Uma hipótese por iteração.
- Diff pequeno (menos de 50 linhas).
- Reverter imediatamente o que for rejeitado.
- Registrar cada iteração no `log.md` e cada ciclo em `log_loop.md`.

## LIMITES DE PARADA

- Máximo: 20 iterações (fonte de máquina: `config_loop.json` -> `limites`).
- Parada antecipada: meta atingida OU 5 rejeições consecutivas OU falta de
  hipóteses plausíveis.

## ESCOPO FECHADO (não fazer mesmo se der vontade)

- Não adicionar comandos além dos aprovados (`/start`, `/dolar`, `/selic`, `/ipca`,
  `/poupanca`).
- Não adicionar webhook, banco, autenticação de usuário, cache em disco ou dependência paga.
- Ideia fora do escopo vai para `NOTES.md`, seção "Ideias futuras".
