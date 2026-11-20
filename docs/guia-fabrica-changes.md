# Guia de uso da fábrica de software para changes

Este guia apresenta um roteiro para conduzir uma change com Codex, OpenSpec, PentaPRO e as skills Teknolista. Adapte-o às regras do repositório e à complexidade da alteração. A fábrica é um fluxo orientado por instruções e agentes; seus resultados dependem das ferramentas, permissões, modelos e verificações disponíveis em cada execução.

## 1. Preparar o projeto uma vez

- [ ] Abra uma sessão do Codex no repositório correto e confira a branch e as alterações locais existentes.
- [ ] Instale as skills necessárias no escopo do projeto: pelo menos `setup-pentapro`, `software-factory`, `penta-pro`, `software-delivery`, `peer-review` e `git-ship`, além das skills especializadas que o projeto utiliza.
- [ ] Peça: **“Use `$setup-pentapro` para configurar este repositório para a fábrica de software. Use somente instalações e configurações locais ao projeto e preserve as escolhas existentes. O objetivo deste repositório é [descrição do projeto].”**
- [ ] Escolha se deseja substituir, complementar ou preservar o README existente. Se ele for gerado ou atualizado, indique o idioma. Escolha uma licença quando o projeto ainda não tiver uma.
- [ ] Examine o relatório do setup: instruções, regra de registro de prompts, tracker, documentos de domínio, OpenSpec, skills e agentes. Resolva as pendências que afetem a change. A regra de registro depende da observância pelo agente; sua existência não comprova captura automática.
- [ ] Confira a versão do OpenSpec, o schema e a localização das skills instaladas. A versão e suas opções de instalação devem permitir confirmar que o setup é restrito ao projeto. Em projetos existentes, preserve configurações e personalizações.
- [ ] Em Codex, confira os papéis locais e ajuste `model` e `model_reasoning_effort` nos arquivos de `.codex/agents/` conforme os modelos disponíveis. Os templates incluem `factory_spec`, `factory_implementer`, `factory_verifier`, `factory_reviewer` e `factory_retrospective`. Reinicie ou abra uma nova sessão se necessário e confirme a descoberta; a existência dos arquivos não prova que os agentes foram utilizados.
- [ ] Para um novo produto ou uma especificação ainda não consolidada, use `$penta-pro` para registrar o problema, os usuários, o primeiro resultado útil e as decisões conhecidas. Uma especificação pronta, por si só, não autoriza implementação ou publicação.

## 2. Solicitar a change

Descreva o comportamento desejado, quem será afetado, os limites, exemplos de sucesso e erro, requisitos de compatibilidade e o que não faz parte do pedido. Nomeie as operações que deseja que a fábrica execute. Este exemplo autoriza implementação, revisão, commit, push e arquivamento; adapte-o ao seu caso:

```text
Use $software-factory e os agentes locais disponíveis para esta change.

Objetivo: [resultado que o usuário deve conseguir].
Contexto e restrições: [informações relevantes e registros existentes].
Critérios: [comportamento esperado, exemplos e falhas relevantes].
Fora do escopo: [o que não deve mudar].

Crie e revise a change OpenSpec, use PentaPRO e as skills especializadas
aplicáveis, implemente, verifique e peça revisão independente. Corrija os
problemas confirmados e revalide. Atualize os registros afetados. Faça commit
e push da branch [nome] para [remoto], arquive a change quando estiver pronta,
publique também as alterações do arquivamento e faça uma retrospectiva.
Informe o estado da CI e as verificações indisponíveis.
```

Se desejar somente um plano ou execução local, diga isso e omita as operações não solicitadas. Merge, release, deploy e mudanças em serviços externos precisam estar abrangidos pela autorização aplicável. O agente deve respeitar autorizações já dadas e as regras do projeto.

## 3. Acompanhar especificação e implementação

- [ ] Confirme que a change ativa e o schema do OpenSpec foram identificados e que os critérios descrevem comportamento observável, incluindo casos negativos relevantes.
- [ ] Confira se regras de produto e decisões de arquitetura apontam para seus registros canônicos em PentaPRO, OpenSpec ou nos documentos adotados pelo projeto. Questões que mudem materialmente o resultado devem ser resolvidas antes das tarefas dependentes.
- [ ] Conclua a revisão de especificação exigida antes de enviar trabalho dependente ao implementador. Identifique a revisão da change e a raiz do store quando houver um selecionado.
- [ ] Verifique se o plano divide o trabalho em entregas pequenas, cada uma com resultado, caminhos afetados e forma de verificação. O orquestrador pode executar etapas independentes em paralelo quando não houver conflito de escrita.
- [ ] Peça evidências de testes adequados à change e, quando necessário, execução no alvo real, como navegador, dispositivo, serviço ou ambiente de teste. Validação estrutural do OpenSpec não comprova o comportamento do aplicativo.

## 4. Revisar e concluir

- [ ] Confira o resultado do revisor para o estado integrado: achados, evidências, cobertura e limitações. Uma revisão independente exige um contexto separado; caso não esteja disponível, registre essa limitação.
- [ ] Para cada defeito confirmado, confira a correção, a repetição das verificações afetadas e a nova revisão da versão corrigida. Uma mudança posterior pode invalidar evidências anteriores.
- [ ] Confirme que especificações, tarefas OpenSpec, PentaPRO e documentação afetada correspondem ao resultado e que verificações obrigatórias estão concluídas ou registradas como pendentes.
- [ ] Depois do arquivamento, examine a especificação consolidada, preencha eventuais propósitos gerados como pendentes e valide novamente o resultado com a versão instalada do OpenSpec.
- [ ] Se solicitados, confira o commit, o destino do push, a revisão publicada e o resultado da CI. Verifique se a change foi arquivada e se os arquivos gerados pelo arquivamento também foram publicados quando isso estiver no escopo. Uma revisão publicada antes do arquivamento não contém as alterações feitas depois dele.
- [ ] Leia a retrospectiva: escopo, fontes, revisões, etapas, problemas, retrabalho, intervenções, evidências e melhorias propostas. Trate métricas não observadas como desconhecidas. Se houver uma etapa solicitada pendente, a retrospectiva é provisória; retome-a após a conclusão.
- [ ] Caso a retrospectiva seja adicionada ao Git após a última publicação, inclua sua publicação no escopo quando desejar que ela fique no remoto. Registre o commit resultante.

## 5. Retomar trabalho interrompido

Informe o nome da change e peça ao agente que reabra os arquivos canônicos e o registro da execução, identifique a revisão atual, os resultados ainda válidos, os bloqueios e a próxima ação autorizada. Confirme cada etapa pelas evidências da revisão correspondente. Após uma interrupção em push ou archive, confira a referência remota, a pasta da change e as especificações consolidadas antes de repetir a operação. Mantenha o store e a raiz de planejamento selecionados na retomada.

Consulte a [skill Software Factory](../software-factory/SKILL.md), seu [contrato de execução](../software-factory/references/execution.md), o [protocolo de retrospectiva](../software-factory/references/retrospective.md), o [procedimento de setup](../setup-pentapro/references/factory-setup.md) e a [retrospectiva do primeiro piloto](retrospectiva-piloto-fabrica-2026-11-19.md) para detalhes e limitações.
