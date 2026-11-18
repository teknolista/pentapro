# Política de registro de prompts

Regra obrigatória para todos os agentes e modelos que trabalham neste repositório. A versão operacional e resumida fica no `AGENTS.md` que o harness carrega (nesta máquina, `~/.config/opencode/AGENTS.md`); este documento detalha formato, mecanismo, limites e decisões.

## Regra

Todo prompt enviado a qualquer agente de IA **deve** ser anexado ao `AGENTS.log` na raiz do repositório antes da requisição ao modelo que o executa. Nenhum prompt deve chegar ao modelo sem estar registrado. Se o registro falhar, o trabalho deve parar, a gravação deve ser corrigida e os prompts pendentes devem ser registrados antes de continuar.

- **Escopo:** todas as interações, sem exceção, incluindo prompts enviados a subagentes.
- **Integridade:** apenas anexação incremental; nunca reescrever, reordenar ou apagar entradas.
- **Sigilo:** segredos e dados pessoais não devem ser colados nos prompts; quando chegarem mesmo assim, devem ser substituídos por `[REDACTED]` antes do registro.
- **Silêncio:** o registro não gera mensagem de confirmação na conversa; apenas falhas são reportadas.
- **Versionamento:** o log é **local**. Está no `.gitignore`, nunca é commitado e não deve ser publicado.

## Formato

Cada entrada tem um cabeçalho e o texto integral do prompt:

```markdown
## Tue, 17 Nov 2026 13:37:31 -0300 | opencode/deepseek-v4.1-flash-free (agent plan)
"texto integral do prompt, com espaçamento e quebras de linha preservados"

```

- **Data e hora:** RFC 5322 em hora local, com fuso, por exemplo `Tue, 17 Nov 2026 13:37:31 -0300`.
- **Agente/modelo:** `provedor/modelo` e, entre parênteses, o agente que o recebeu. O identificador do provedor elimina ambiguidade entre modelos de mesmo nome.
- **Corpo:** o prompt exatamente como enviado; o texto não é reescrito, resumido nem reformatado.
- **Separador:** uma linha em branco depois do corpo. Entradas consecutivas são separadas por essa linha.

Anexos aparecem como `[anexo: <nome>]` na posição em que foram enviados, porque o conteúdo binário não é texto.

## Como o registro acontece

### Captura automática (OpenCode)

O plugin de projeto `.opencode/plugins/agents-log.ts` registra os prompts sem depender da obediência do modelo:

1. Assina o hook `context` da sessão, que roda imediatamente antes de cada requisição ao modelo.
2. Percorre as mensagens da requisição e seleciona apenas prompts reais do usuário. Mensagens injetadas pelo próprio harness chegam com papel `user` e se distinguem pelo `metadata`: o lembrete do modo *plan* não tem `metadata`, o checkpoint de conversa traz `keepID`/`recent` e o prompt real traz `{}` (CLI) ou `{displayText}` (TUI). Um segundo filtro rejeita texto iniciado por `<system-reminder>`, `<context>`, `<environment_context>` ou `<conversation-checkpoint>`.
3. Anexa a entrada com `append`, de forma síncrona, antes de a requisição seguir para o modelo. Se a anexação falhar, o plugin lança um erro e a requisição é abortada: o prompt não chega ao modelo sem estar registrado.
4. Mantém em memória os identificadores das mensagens já registradas, para não repetir o mesmo prompt nas etapas seguintes da execução. Não há arquivo de estado: reiniciar o servidor e retomar a sessão pode registrar novamente prompts antigos, o que é aceito nesta versão inicial.

Verificado em OpenCode 2.0.31 no Linux; a API do plugin é interna a essa versão e precisa ser revalidada em qualquer atualização.

### Registro manual (outros harnesses)

Nas ferramentas que não carregam o plugin (`CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/`, `.windsurfrules` apenas declaram a regra), o próprio agente anexa a entrada como primeira ação da sessão, no formato acima. Nesse caso o registro depende da obediência do modelo e não há garantia mecânica.

**Não registre duas vezes.** Quando o harness já registra automaticamente, a tarefa é verificar a entrada, não criá-la.

## Segurança

A redação é **melhor esforço** e cobre padrões usuais: chaves privadas PEM, chaves `sk-`/`rk-`/`pk-`, tokens `ghp_`/`github_pat_`, chaves `AKIA`, chaves `AIza`, tokens `xox*`, JWT, `Bearer`, e valores após `senha`, `password`, `token`, `secret` ou `api_key`. Ela não identifica dados pessoais nem formatos desconhecidos. Continua proibido colar segredos em prompts, e um segredo que chegue ao log deve ser revogado, não apenas apagado — o arquivo é local, mas o valor já circulou.

## Concorrência

O log usa abertura em modo de anexação (`O_APPEND`), o que evita que agentes simultâneos sobrescrevam a posição de escrita uns dos outros. A ordem entre entradas concorrentes não é garantida e uma entrada muito grande pode ser intercalada com outra. Para auditoria, considere o conjunto, não a ordem absoluta.

## Limites conhecidos

- Prompts que nunca chegam a uma requisição ao modelo (por exemplo, cancelados antes do envio) não são registrados.
- O hook depende de a API de plugins do harness continuar oferecendo o evento usado; uma atualização do OpenCode pode exigir ajuste e revalidação.
- A deduplicação é apenas em memória: reiniciar o servidor e retomar a sessão registra novamente os prompts antigos. Duplicatas são aceitas nesta versão inicial.
- Não há rotação automática: o arquivo cresce sem limite. A rotação é manual, por cópia do arquivo e recomeço do log; entradas nunca são editadas.
- O arquivo foi reiniciado em 2026-11-17, depois de a correção do filtro entrar em vigor. A versão anterior ficou em `AGENTS.log.pre-fix` (também ignorada pelo Git) e contém entradas de teste e checkpoints registrados por engano.
- Textos anteriores a esta política (por exemplo, o conteúdo de `AGENTS.md` que ocupava o arquivo) não são histórico de prompts e não foram apagados por causa da regra de anexação apenas.
- O plugin e os arquivos dos demais harnesses são artefatos locais de desenvolvimento: `.opencode/`, `.cursor/` e `.windsurfrules` estão no `.gitignore`. Neste repositório, o único arquivo de instrução versionado é o template `AGENTS-template.md`; o `AGENTS.md` de trabalho e os arquivos equivalentes dos outros harnesses ficam fora do Git quando existem.

## Decisões

- A regra vive no `AGENTS.md` que o harness carrega, porque é esse o arquivo lido em toda requisição; um documento solto em outro caminho não seria lido.
- O detalhe fica neste documento para manter o `AGENTS.md` curto, já que ele é enviado em toda requisição.
- O log não é versionado por decisão do dono: evita dados pessoais, crescimento e conflitos no histórico do Git.
- A falha de gravação aborta a requisição em vez de seguir sem registro, porque a regra proíbe executar prompt não registrado.
- Não há arquivo de estado: o dono dispensou o controle persistente de duplicatas nesta versão inicial. O log fica sozinho na raiz e é ignorado pelo Git.

## Evidência

Verificado em 2026-11-17 no Linux, com OpenCode 2.0.31 e o modelo `opencode/deepseek-v4.1-flash-free`:

- Prompt de uma linha, prompt multilinha e anexo de arquivo registrados na íntegra.
- Redação aplicada a `senha:` e a uma chave `sk-`.
- Uma execução com chamada de ferramenta gerou uma única entrada, apesar de várias requisições ao modelo.
- Sessão retomada com `--continue` registrou o novo prompt e repetiu o anterior, como esperado pela deduplicação apenas em memória; nenhum arquivo de estado foi criado.
- Com o log sem permissão de escrita, a execução foi abortada com erro `[agents-log] falha ao gravar ...` e nada foi enviado ao modelo.
- Lembrete injetado pelo modo *plan* e checkpoint de conversa não foram registrados.
- Teste unitário com Bun, executado sobre uma cópia do próprio arquivo do plugin, cobriu a seleção de mensagens (prompt de CLI, prompt de TUI, checkpoint, lembrete de *plan* com e sem `metadata`, assistente, ferramenta e sistema), o formato RFC 5322, o marcador de anexo e a redação de `senha:`, `Bearer`, `sk-` e `ghp_`; todos os casos passaram.
