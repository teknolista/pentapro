
USO DE PENTAPRO EM PROJETOS GREENFIELD e BROWNFIELD:

Passo 0: Desenvolvedor instala plugin pentapro e realiza configuração inicial com setup-pentapro.


CENÁRIO 1: Início de projeto (greenfield), sem especificação na pasta "/pentapro"

* Passo 1.1: Desenvolvedor aciona agente de exploração no prompt e explica pro agente o que pretente desenvolver, respondendo a todos os questionamentos do agente. O interrogatório é feito para identificar tudo o que será necessário para especificar as 5 dimensões do software: PRODUCT, PRODUCTION, PROOF, PROJECT, PROCESS.

* Passo 1.2: agente cria um nome para designar essa implementação inicial e salva uma pasta com esse nome em "/pentapro/changes". O detalhamento obtido da exploração é usado para criar a especificação inicial do software que será salva em artefatos na pasta "/pentapro/changes".

* Passo 1.3: Após realizar todo o detalhamento da especificação, agente aciona outro agente para revisar a especificação e verificar se está seguindo o padrão de pentapro. Se houver erros ou necessidade de maiores esclarecimentos, novas perguntas são feitas ao desenvolvedor para atualizar os artefatos criados até então dentro da change.

* Passo 1.4: Estando tudo ok, agente aciona o agente responsável pela implementação. o agente de implementação consulta as especificações e inicia planejamento das tarefas necessárias. Em seguida já inicia a execução das tarefas. Esta etapa é bem semelhate à correspondente do OpenSpec. Todas as nossas skills voltadas a implementação e testes podem ser acionadas nesse passo.

* Passo 1.5: Finalizada a implementação, é acionado o(s) agente(s) para revisão dos trabalhos. Se houver algum problema, retorna para o agente de implementação fazer correções e novos testes. Em seguida, aciona novamente o agente de revisão e fica em loop até concluir toda a change e atender a todos os critérios de aceitação.

* Passo 1.6: Quando a change for considerada pronta, notifica o desenvolvedor para que ele valide a change e dê feedback ao agente. Se o feedback for negativo, então é acionado o agente explorado para coletar novas informações ou especificações, alterar o planejamento, criar novas tarefas, realizar correções, fazer revisão e então notificar novamente o desenvolvedor. Fica em loop até o desenvolvedor confirmar a finalização da change.

* Passo 1.7: Desenvolvedor aciona agente e notifica que pode arquivar a change. O agente seguirá processo semelhante ao do OpenSpec, sincronizando toda a especificação da change nas 5 dimensões de especificação principais da pasta "/pentapro". Em seguida, move as changes concluídas e consideradas arquivadas para a subpasta "/pentapro/changes/archive". Uma vez que as changes estiverem arquivadas e a documentação principal do pentapro do projeto estiver corretamente sincronizada com a change, o agente software-shipper é acionado para publicar todas as mudanças no repositório remoto (commit e push).

---

CENÁRIO 2: Retomada de projeto (greenfield ou brownfield), adição de nova feature ou modificação de feature existente

* Passo 2.1: Desenvolvedor aciona agente de exploração no prompt e explica pro agente o que pretente adicionar, alterar ou remover, respondendo a todos os questionamentos do agente. O interrogatório é feito para identificar tudo o que será necessário para especificar as 5 dimensões do software: PRODUCT, PRODUCTION, PROOF, PROJECT, PROCESS.

* Passo 2.2: agente cria um nome para designar essa nova change e salva uma pasta com esse nome em "/pentapro/changes". O detalhamento obtido da exploração é usado para criar a especificação da change será salva em artefatos na pasta "/pentapro/changes".

* Passo 2.3: Após realizar todo o detalhamento da especificação da change, agente aciona outro agente para revisar a especificação e verificar se está seguindo o padrão de pentapro. Se houver erros ou necessidade de maiores esclarecimentos, novas perguntas são feitas ao desenvolvedor para atualizar os artefatos criados até então dentro da change.

* Passo 2.4: Estando tudo ok, agente aciona o agente responsável pela implementação. o agente de implementação consulta as especificações e inicia planejamento das tarefas necessárias. Em seguida já inicia a execução das tarefas. Esta etapa é bem semelhate à correspondente do OpenSpec. Todas as nossas skills voltadas a implementação e testes podem ser acionadas nesse passo.

* Passo 2.5: Finalizada a implementação, é acionado o(s) agente(s) para revisão dos trabalhos. Se houver algum problema, retorna para o agente de implementação fazer correções e novos testes. Em seguida, aciona novamente o agente de revisão e fica em loop até concluir toda a change e atender a todos os critérios de aceitação.

* Passo 2.6: Quando a change for considerada pronta, notifica o desenvolvedor para que ele valide a change e dê feedback ao agente. Se o feedback for negativo, então é acionado o agente explorado para coletar novas informações ou especificações, alterar o planejamento, criar novas tarefas, realizar correções, fazer revisão e então notificar novamente o desenvolvedor. Fica em loop até o desenvolvedor confirmar a finalização da change.

* Passo 2.7: Desenvolvedor aciona agente e notifica que pode arquivar a change. O agente seguirá processo semelhante ao do OpenSpec, sincronizando toda a especificação da change nas 5 dimensões de especificação principais da pasta "/pentapro". Em seguida, move as changes concluídas e consideradas arquivadas para a subpasta "/pentapro/changes/archive". Uma vez que as changes estiverem arquivadas e a documentação principal do pentapro do projeto estiver corretamente sincronizada com a change, o agente software-shipper é acionado para publicar todas as mudanças no repositório remoto (commit e push).

--------------------------------------------------------------------------------
