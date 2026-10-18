# Base de trabalho: `projeto_loop`

Este projeto **nasce do modelo** [`projeto_loop`](https://github.com/Georgebecker/projeto_loop).
A base não é inspiração: é a origem dos arquivos de método que estão aqui. Se algo deste
documento divergir da base, a base manda — exceto onde este projeto tem motivo escrito
para divergir (seção "Diferenças conscientes").

## Origem

| Item | Valor |
|---|---|
| Repositório | <https://github.com/Georgebecker/projeto_loop> |
| Caminho local na máquina | `D:\Projetos\projeto_loop` |
| Commit de referência da sincronização | `8830840ab9644f1f4f19c104ae9d6396bf0a5d52` |
| Data do commit da base | 2026-10-14 |
| Data desta sincronização | 2026-10-18 |

## O que veio da base

| Arquivo / pasta | Papel |
|---|---|
| `docs/REGRAS_DE_OURO.md` | Contrato de qualidade (postura, processo, técnica, Loop Engineering, checklist de dados). |
| `docs/GUIA_NOVO_PROJETO.md` (não copiado aqui) | Guia de criação de novos projetos; vive na base. |
| `.githooks/pre-commit`, `.githooks/pre-push`, `.githooks/instalar.ps1`, `.githooks/README.md` | Barreira que impede `.env` e segredo no commit e no envio. |
| `.gitattributes` | `text eol=lf` nos ganchos. |
| `requirements.txt` | Dependências Python, com versão exata. |
| `LICENSE` (MIT), `.gitignore`, `.env.example` | Estrutura mínima de projeto. |
| `data/raw/`, `data/processed/`, `data/descartados/`, `notebooks/` | Pastas de dados, só com `.gitkeep`. |
| `meu-loop-agente/` | O cérebro do loop: `program.md` (contrato), `config_loop.json` (máquina), `system_prompt.md` (comportamento), `log.md`, `baseline.json`, `outputs/`, `workspace/` e `verificar_iteracao.py`. |

## Diferenças conscientes

| Item | Base | Aqui | Por quê |
|---|---|---|---|
| `meu-loop-agente/config_loop.json` | exemplo Next.js (`npm run …`, bundle em kB) | `python -m pytest -q` e métrica "testes que passam" | Não há sistema alvo; a métrica provisória mede a saúde da base. |
| `meu-loop-agente/program.md` | redução de bundle Next.js | objetivo provisório de infraestrutura | O contrato do produto ainda não chegou. |
| `meu-loop-agente/system_prompt.md` | escopo restrito a `workspace/` | escopo conforme `program.md` | Aqui o contrato precisa poder apontar para `tests/` e `docs/` enquanto não há produto. |
| `meu-loop-agente/workspace/` | `app/`, `components/`, `lib/` de exemplo | vazio, com `LEIA-ME.md` | Remove andaime de Next.js que não se aplica. |
| `AGENTS.md`, `NOTES.md`, `log_loop.md`, `.github/` | não existem na base | existem aqui | Regras do agente, decisões e customizações locais. |
| `.env.example` | modelo genérico da base | modelo do template global (mais campos, sem valores) | O `.env.example` do template global é o padrão desta máquina. |
| `scripts/criar_projeto_base.ps1` | cria projeto a partir da base | **não copiado** | O script copia a partir da pasta-mãe; dentro deste projeto ele criaria um projeto a partir de si mesmo. Ele vive na base. |
| `docs/GUIA_NOVO_PROJETO.md` | guia de criação | **não copiado** | É manutenção da base, não do projeto derivado. Este documento substitui a consulta no dia a dia. |
| `docs/REGRAS_DE_OURO.md` | termina no "Resumo em uma frase" | recebeu a **Parte V — Didática obrigatória** ao final | O dono exigiu que ensinar fosse regra do projeto. O texto da base continua intacto no começo do arquivo; `scripts/conferir_base.py` confere que o conteúdo original permanece como prefixo (acréscimo no final é permitido; edição do original, não). |

## Como não esquecer (mecanismo)

1. `AGENTS.md` tem a seção **Base de trabalho** logo no início — é lida em toda sessão.
2. `.github/copilot-instructions.md` repete o atalho.
3. `python scripts/conferir_base.py` confere em segundos: arquivos da base presentes,
   Regras de Ouro e ganchos idênticos, `core.hooksPath` ativo, `.env` ignorado e nenhum
   valor de chave em arquivo.
4. `tests/test_base_projeto_loop.py` transforma essa conferência em teste: se a âncora
   se perder, a suíte fica vermelha.

## Re-sincronizar com a base

```powershell
# 1. ver o que a base tem de novo
cd D:\Projetos\projeto_loop
git pull

# 2. conferir o que falta ou divergiu aqui
cd D:\Projetos\bot-indicadores
python scripts/conferir_base.py

# 3. copiar só o que é método (nunca sobrescrever o contrato local sem ler)
Copy-Item D:\Projetos\projeto_loop\docs\REGRAS_DE_OURO.md docs\ -Force
Copy-Item D:\Projetos\projeto_loop\.githooks\* .githooks\ -Force
```

Depois de re-sincronizar, atualize o commit de referência nesta tabela e registre a
decisão em `NOTES.md`.
