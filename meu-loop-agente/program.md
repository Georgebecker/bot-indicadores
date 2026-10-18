# Loop Program — bot-indicadores

> Este arquivo é o CONTRATO do agente. Só o humano altera.
> Os números ficam em `baseline.json`; comandos e medição, em `config_loop.json`.
> Mantenha os três coerentes entre si.
>
> **Estado:** contrato do produto ainda não recebido. O objetivo abaixo é provisório e
> cobre apenas a infraestrutura da base. Quando o contrato chegar, este arquivo é
> substituído antes de qualquer código de produto.

## OBJETIVO (provisório)

Manter a base do projeto saudável e verificável enquanto o contrato do bot de
indicadores não chega: aumentar a quantidade de testes automatizados que passam, sem
quebrar nenhum teste existente e sem implementar funcionalidade de produto.

## BASELINE E META

- Fonte dos números: `baseline.json` (valor inicial, melhor valor, meta).
- Métrica provisória: quantidade de testes que passam (`python -m pytest -q`).
- Meta: cada ciclo precisa aumentar o número de testes que passam ou, no mínimo,
  mantê-lo com um teste novo que cubra uma regra escrita do projeto.

## ARQUIVOS PERMITIDOS (o agente só mexe aqui)

- `tests/**`
- `scripts/**`
- `docs/**`
- `README.md`
- `NOTES.md`
- `log_loop.md`

## ARQUIVOS PROIBIDOS

- `.env`, `.env.example`, segredos e credenciais (qualquer valor de chave)
- `.githooks/**`
- `AGENTS.md`, `.github/**`
- `meu-loop-agente/program.md`, `meu-loop-agente/config_loop.json`,
  `meu-loop-agente/system_prompt.md`
- `src/**` enquanto o contrato do produto não existir
- Qualquer caminho fora do repositório

## COMANDOS DE VERIFICAÇÃO (obrigatórios)

- Fonte de máquina: `config_loop.json` -> `verificacao.comandos` (não duplicar aqui,
  para não divergir).
- Conteúdo atual: `python -m pytest -q`.

## MÉTRICA PRINCIPAL

- Nome: quantidade de testes que passam.
- Direção: maior é melhor.
- Comando e leitura do número: `config_loop.json` -> `metrica`.

## MÉTRICAS SECUNDÁRIAS (não podem piorar)

- Quantidade de testes que falham ou geram erro: zero.
- `python scripts/conferir_base.py` precisa continuar saindo com código 0.

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
- Registrar cada iteração no `log.md` (hipótese, arquivos, métricas, decisão).

## LIMITES DE PARADA

- Máximo: 20 iterações (fonte de máquina: `config_loop.json` -> `limites`).
- Parada antecipada: meta atingida OU 5 rejeições consecutivas OU falta de
  hipóteses plausíveis.
