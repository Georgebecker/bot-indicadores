# Como ler este código (guia para quem está começando)

Este guia existe porque o projeto foi escrito para ser **lido**, não só executado.
Se você sabe `if`, `for` e funções, aqui está o resto do vocabulário — em linguagem
simples, com analogia para cada ideia.

## Antes de tudo: por onde começar

1. [`src/bot_indicadores/config.py`](../src/bot_indicadores/config.py) — o token e o endereço.
2. [`src/bot_indicadores/formatacao.py`](../src/bot_indicadores/formatacao.py) — números em português.
3. [`src/bot_indicadores/bcb.py`](../src/bot_indicadores/bcb.py) — a conversa com o Banco Central.
4. [`src/bot_indicadores/handlers.py`](../src/bot_indicadores/handlers.py) — o que o bot responde.
5. [`src/bot_indicadores/app.py`](../src/bot_indicadores/app.py) — como tudo é ligado.

## Palavras que aparecem no código

### API

Um **balcão de atendimento** de outro programa. Você faz um pedido (uma URL), ele
responde com dados. Aqui, o balcão é o Banco Central, e o pedido é "me dê os últimos
valores da série 432".

### JSON

Uma forma de escrever dados que qualquer linguagem entende. Parece um dicionário:

```json
[{"data": "01/10/2026", "valor": "5.2079"}]
```

Lê-se: "uma lista com um item, que tem data e valor". É o que o BCB devolve.

### HTTP e códigos de status

O número que vem junto da resposta:

| Código | Em palavras |
|---|---|
| 200 | "Deu certo" |
| 400–499 | "Seu pedido está errado" (URL errada, sem permissão) |
| 500–599 | "O problema é do meu lado" (servidor fora do ar) |

Detalhe que confunde muita gente: o Banco Central às vezes responde **200** com um
erro escrito dentro do JSON. Por isso o código confere o conteúdo, não só o número.

### Assíncrono (`async` / `await`)

Uma fila de padaria com uma atendente só. Enquanto o pão de um cliente assa, ela
atende o próximo. **Assíncrono** é isso: não ficar parado esperando.

No código, `async def` marca a função que pode esperar; `await` marca o ponto de
espera. Quem chama um comando de Telegram não fica bloqueado enquanto consultamos o
Banco Central.

### `asyncio.to_thread`

Se a função é "bloqueante" (fica parada esperando, como a biblioteca `requests`),
ela não pode rodar na fila principal — travaria a atendente. `to_thread` manda essa
tarefa para uma segunda linha de atendimento.

### Cache

Um **bilhete com a resposta que acabou de chegar**, preso no balcão. Se alguém fizer
a mesma pergunta em menos de 60 segundos, a atendente lê o bilhete em vez de ligar
de novo para o Banco Central. O bilhete tem validade: passou de 60 s, é jogado fora.

### Timeout e retry

**Timeout** é o tempo máximo que esperamos antes de desistir. **Retry** é tentar de
novo, uma vez, porque rede oscila. Desistir rápido é gentileza com quem está no chat.

### Injeção de dependência

Em vez de a classe criar sozinha a conexão com o mundo, ela **recebe** essa conexão
de fora. Assim os testes entregam um "Banco Central de mentira" e nada toca a
internet.

### Mock (dublê)

Um ator substituto no ensaio. Nos testes, `SessaoFalsa` e `ClienteFalso` fingem ser
o site e o Banco Central, devolvendo exatamente a resposta que queremos testar.

### Teste

Uma frase que o computador verifica sozinho. `assert` significa "isto precisa ser
verdade". Se não for, o teste fica vermelho e mostra o porquê.

## Como o projeto decide o que manter

Cada melhoria entra com uma **métrica antes e depois** (registrada em `MEMORIA.md`, um
arquivo local). Se não melhorou, é revertida. É por isso que existe
o [`meu-loop-agente/`](../meu-loop-agente/).

## Onde pedir ajuda

Abra uma issue — inclusive para dizer "não entendi este arquivo". Comentário que não
ensina é bug de didática, e a [Parte V das Regras de Ouro](REGRAS_DE_OURO.md) trata
isso como regra do projeto.
