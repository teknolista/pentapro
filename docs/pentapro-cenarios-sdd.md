# Cenários de SDD nativo com PentaPRO

Este guia complementa o [checklist operacional da fábrica](guia-fabrica-changes.md). A sessão principal é o agente de exploração e orquestração; os seis especialistas são acionados quando necessários e disponíveis no host. Os nomes lógicos, como `factory_shipper`, precisam ser resolvidos para os identificadores descobertos pelo ambiente.

## Preparação comum

Instale uma única fonte da coleção por host/projeto e execute `setup-pentapro` no repositório correto. Preserve instruções, configurações, logs e personalizações. Confira a descoberta dos agentes e os modelos/esforços selecionados. Arquivos instalados não demonstram execução nem isolamento de permissões.

O setup prepara a estrutura, mas não cria uma change fictícia nem aceita requisitos. O fluxo usa `pentapro/` na raiz do repositório. A especificação segue PRODUCT, PROJECT, PRODUCTION, PROOF e PROCESS. Cada change ativa possui seis arquivos: `change.md`, `product.md`, `project.md`, `production.md`, `proof.md` e `process.md`.

Para solicitar implementação pela fábrica, descreva o resultado e a autoridade pretendida:

```text
Use software-factory para especificar e implementar este incremento: [resultado].
Preserve as decisões existentes e apresente o resultado verificado para minha aceitação.
```

Se pedir somente exploração ou especificação, o trabalho termina nesse escopo; uma especificação revisada não autoriza implementação por si só.

## Cenário 1: projeto novo, sem especificação consolidada

1. **Explorar.** A sessão principal identifica usuário, problema, resultado observável, restrições e decisões relevantes. Ela aproveita informações existentes e pergunta apenas o necessário para resolver incertezas que afetem o incremento.
2. **Salvar a proposta.** O agente cria `pentapro/changes/<nome>/` com os seis arquivos. Os tópicos da raiz permanecem modelos pendentes até a consolidação aprovada. A proposta distingue fatos confirmados, sugestões e questões abertas.
3. **Revisar a especificação.** `factory_spec` reconstrói a jornada, examina as cinco dimensões e aponta ambiguidades, riscos e critérios sem verificação viável. O orquestrador resolve os achados e preserva decisões ainda pendentes. Se a revisão independente obrigatória não puder ocorrer, esse gate permanece incompleto.
4. **Planejar e implementar.** Quando a implementação estiver autorizada, a sessão principal usa `software-delivery` para organizar tarefas delimitadas. `factory_implementer` aplica as skills pertinentes e produz mudanças e verificações proporcionais aos critérios. Cada tarefa identifica arquivos de responsabilidade e dependências; o projeto não precisa executar todas as skills.
5. **Verificar e revisar.** `factory_verifier` confere critérios e evidências no snapshot integrado. `factory_reviewer` procura defeitos sustentados por evidência em contexto separado quando disponível. Achados retornam ao responsável pela correção. Limite as tentativas repetidas para a mesma falha conforme o protocolo da fábrica; diante de falta de progresso, reavalie a causa e registre o bloqueio, em vez de manter um loop ilimitado.
6. **Apresentar para aceitação.** O orquestrador informa o resultado, o que foi realmente verificado, lacunas e efeitos pendentes. Feedback que altera requisitos atualiza a change e reabre apenas os gates afetados. A confirmação do desenvolvedor, e não o parecer de um agente ou o silêncio, estabelece aceitação.
7. **Consolidar e entregar.** Por padrão, uma aprovação explícita do resultado verificado autoriza consolidar os requisitos nos tópicos da raiz, arquivar em `pentapro/changes/archive/YYYY-MM-DD_<nome>/`, commitar e fazer push normal. Respeite instruções mais restritas, como entrega somente local ou aprovações separadas. O orquestrador reconcilia os cinco pilares antes do arquivo; `factory_shipper`, usando `git-ship`, revisa o conjunto e confirma o SHA no destino real. Merge, release e deploy mantêm sua própria autoridade.

## Cenário 2: projeto existente, nova feature ou alteração

O ciclo de revisão, implementação autorizada, verificação, aceitação e entrega é o mesmo. A diferença está na referência inicial:

1. Leia os contratos, consumidores, dados e comportamento atuais. Identifique a revisão e as diferenças locais relevantes. Se não houver PentaPRO, registre as fontes que ainda governam o projeto; não invente uma baseline aceita.
2. Preserve a especificação consolidada enquanto a mudança é proposta e implementada em `pentapro/changes/<nome>/`. Identifique requisitos adicionados, modificados, removidos ou renomeados, preservando IDs e cenários não afetados.
3. Nas dimensões sem impacto, explique por que permanecem iguais e aponte para seu registro real. Nas dimensões afetadas, registre compatibilidade, migração, recuperação, critérios e verificações necessárias.
4. Depois da aceitação explícita, confira cada alteração contra a baseline anterior, reconcilie os cinco pilares e verifique os links a partir do destino de arquivo. Um movimento de pasta bem-sucedido não demonstra consistência nem funcionamento do software.

## Retomada, cancelamento e melhoria contínua

Em trabalho substancial ou com agentes da fábrica, o orquestrador mantém um registro em `docs/agents/runs/<run-id>/`. Reutilize a mesma execução para a mesma tarefa através de prompts, sessões e tentativas. Cada despacho recebe uma identidade e um evento; não crie um diretório por prompt. Apenas o orquestrador escreve o estado, os eventos e as lições.

Na retomada, confira arquivos, evidências e efeitos reais antes de repetir uma operação. Um push confirmado não deve ser repetido só porque faltou registrar o recibo. Arquivos, métricas ou conclusões históricas conservam sua revisão e limites.

Uma change cancelada registra a decisão, efeitos parciais e recuperação necessária, sem promover requisitos abandonados nem reverter código automaticamente. Após a entrega ou um bloqueio relevante, `factory_retrospective` propõe melhorias com evidências; o orquestrador registra as lições em inglês. Mudanças reutilizáveis na coleção precisam de seu próprio escopo e avaliação.

Consulte os contratos atuais de [fábrica](../software-factory/SKILL.md), [PentaPRO](../penta-pro/SKILL.md), [entrega Git](../git-ship/SKILL.md) e [registros de execução](../software-factory/references/run-records.md).
