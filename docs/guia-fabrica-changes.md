# Conduzir uma change com PentaPRO

A sessão principal do ambiente de codificação atua como agente de exploração e orquestração. O desenvolvedor descreve o resultado desejado uma vez; o agente esclarece decisões relevantes e aciona os especialistas durante o trabalho. O processo usa especificações em Markdown e as ferramentas normais do projeto, sem um utilitário de SDD ou schemas configuráveis.

## 1. Preparar o projeto

Instale a coleção e execute `setup-pentapro` no repositório de destino. Confira a preservação das instruções, logs, configurações e agentes personalizados. O setup prepara `pentapro/changes/archive/` e a orientação da fábrica; não inventa uma change ativa nem aceita uma especificação inicial.

Os seis especialistas possuem definições para Codex, Claude Code, Cursor, GitHub Copilot, OpenCode e Antigravity. O ambiente precisa descobrir os perfis e oferecer as ferramentas necessárias. Preserve modelo/esforço configurados e personalizações. Cursor usa nomes como `factory-shipper`; OpenCode usa o identificador do arquivo. Confira o mapeamento do host e não confunda um arquivo instalado com execução comprovada.

## 2. Descrever o trabalho

Exemplo de uma única solicitação:

> Use software-factory para desenvolver um catálogo de serviços com busca e favoritos. Explore os requisitos comigo e conduza a implementação e a verificação.

Para um projeto existente:

> Use software-factory para permitir exportação dos favoritos, preservando o comportamento e os dados existentes.

Pedidos de exploração ou especificação apenas respeitam esse limite. O agente não deve presumir implementação, gastos ou efeitos externos a partir de uma pergunta sobre uma ideia.

## 3. Especificar a change

O agente escolhe uma identidade única de duas ou três palavras minúsculas separadas por hífens e abre `pentapro/changes/<nome>/`. Confere changes ativas e arquivadas para evitar colisões. A change contém seis arquivos:

| Arquivo | Responsabilidade |
| --- | --- |
| change.md | Identidade, problema, escopo, baseline, impactos, estado, aprovação e índice |
| product.md | Requisitos e cenários observáveis, IDs estáveis e comportamento antes/depois |
| project.md | Arquitetura, contratos, decisões, alternativas e riscos |
| production.md | Instalação, operação, compatibilidade, migração e recuperação |
| proof.md | Critérios, verificações planejadas/executadas, evidências e versão testada |
| process.md | Autoridade, tarefas, responsáveis, dependências e retomada |

Uma dimensão não afetada informa isso e aponta para a baseline. Não se inventam requisitos para preencher o modelo. No primeiro projeto, a especificação ainda não existe como baseline aceita: ela é elaborada na change. Nos projetos existentes, os cinco pilares principais continuam representando a baseline consolidada enquanto a mudança é implementada.

## 4. Implementar e revisar

O agente principal aciona a revisão da especificação antes da implementação dependente. Em seguida planeja incrementos, delega escopos delimitados e usa as skills especializadas pertinentes. Cada tarefa tem uma forma observável de verificar sua conclusão; testes e documentação acompanham o incremento responsável.

A verificação liga critérios a evidências reais. A revisão independente examina o snapshot integrado e seus possíveis defeitos. Correções voltam ao implementador e invalidam as evidências afetadas. O fluxo não exige uma sequência de prompts do desenvolvedor, mas perguntas sobre decisões de produto, permissões ou conflitos relevantes continuam necessárias. Tentativas sem progresso são investigadas e limitadas, não repetidas indefinidamente.

## 5. Validar o resultado uma vez

Quando as verificações exigidas passarem, o agente apresenta comportamento, evidências, limitações e efeitos de fechamento pendentes. Por padrão, a aprovação explícita desse resultado autoriza consolidação, arquivamento, commit e push normal da change. O agente informa esse escopo antes de pedir a aprovação.

Se desejar, o desenvolvedor pode pedir etapas separadas ou execução local sem publicação. Essas restrições prevalecem. Aprovar a definição do processo ou a proposta inicial não equivale a aceitar uma implementação ainda não entregue. Silêncio, tempo decorrido e parecer de um modelo não são aprovação humana.

Feedback negativo retorna às decisões, tarefas e verificações afetadas. O agente só apresenta novamente o resultado quando houver evidência atualizada suficiente.

## 6. Consolidar, arquivar e publicar

Após a aprovação, o agente reconcilia o resultado com os cinco pilares principais, preservando requisitos e cenários não alterados. Confere o conteúdo salvo e as evidências afetadas. Move então a pasta para `pentapro/changes/archive/YYYY-MM-DD_<nome>/`, usando a data local do desenvolvedor, e corrige links de entrada e saída. Uma colisão nunca é sobrescrita.

O shipper revisa o snapshot final, cria o commit e faz o push normal dentro da autorização. A referência remota é consultada para confirmar o commit. Arquivamento, publicação, implantação e release são fatos distintos; a aprovação padrão não autoriza merge, deploy, force push ou reescrita de histórico.

Uma change cancelada preserva o motivo, efeitos parciais, decisões de recuperação e trabalho pendente. Não promove intenção abandonada a comportamento entregue nem autoriza rollback automático. Se houver efeitos não reconciliados, o cancelamento fica pendente na change ativa. O arquivo final distingue a disposição `completed` ou `cancelled` de sua localização arquivada.

## 7. Retomar e aprender

Em interrupções, confira os arquivos reais, a branch, a versão testada e os efeitos externos antes de repetir uma operação. Um push ou movimento de diretório pode ter ocorrido mesmo se o registro local falhou. Changes sobre os mesmos requisitos precisam de integração serializada.

O orquestrador mantém um registro durável para execuções substanciais e recolhe candidatos a lições dos agentes. Somente ele escreve o registro de lições, em inglês. O helper existente de registros é opcional e verifica consistência local; não coordena o SDD nem comprova a verdade das evidências. Consulte o [guia de registros](agents/runs/README.md), o [protocolo PDSA](agents/continuous-improvement.md) e o [contrato de fechamento](../software-factory/references/closure.md).
