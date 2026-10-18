# Loop Program — bot-indicadores

> Este arquivo é o CONTRATO do agente. Só o humano altera.
> A métrica é lida do próprio `pytest`; o histórico fica em `MEMORIA.md` (local).
> O verificador automático da base não é versionado aqui — ele é conveniência, não
> requisito: `python -m pytest` já devolve o número.

## OBJETIVO

Manter o bot de Telegram do projeto funcionando e confiável: responder `/start`,
`/dolar`, `/selic` e `/ipca` (e `/poupanca`, aceito no Ciclo 2) com dados da API SGS do
Banco Central, com data de referência, tratamento de falha da API sem quebrar o chat e
token em variável de ambiente ou no `.env` local (que nunca sobe).

## BASELINE E META

- Métrica principal: quantidade de testes que passam (`.venv\Scripts\python.exe -m pytest`).
- Linha de base atual e histórico de ciclos: `MEMORIA.md` (local).
- Eficiência de cache é medida por teste (`tests/test_bcb.py`): duas consultas seguidas do
  mesmo indicador precisam gerar **uma** chamada HTTP.

## ARQUIVOS PERMITIDOS (o agente só mexe aqui)

- `src/**`
- `tests/**`
- `docs/**`
- `README.md`
- `MEMORIA.md` (local, fora do upload)
- `requirements.txt` (com justificativa em `MEMORIA.md`)

## ARQUIVOS PROIBIDOS

- `.env`, `.env.example`, segredos e credenciais (qualquer valor de chave)
- `.githooks/**`
- `AGENTS.md`, `.github/**`
- `meu-loop-agente/program.md`
- Qualquer caminho fora do repositório

## COMANDOS DE VERIFICAÇÃO (obrigatórios)

- `.venv\Scripts\python.exe -m pytest` (a suíte inteira).

## MÉTRICA PRINCIPAL

- Nome: quantidade de testes que passam.
- Direção: maior é melhor; o número sai da última linha do `pytest` ("N passed").

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
- Registrar cada iteração em `MEMORIA.md` (local).

## LIMITES DE PARADA

- Máximo: 20 iterações.
- Parada antecipada: meta atingida OU 5 rejeições consecutivas OU falta de
  hipóteses plausíveis.

## ESCOPO FECHADO (não fazer mesmo se der vontade)

- Não adicionar comandos além dos aprovados (`/start`, `/dolar`, `/selic`, `/ipca`,
  `/poupanca`).
- Não adicionar webhook, banco, autenticação de usuário, cache em disco ou dependência paga.
- Ideia fora do escopo vai para `MEMORIA.md`, seção "Ideias futuras".
