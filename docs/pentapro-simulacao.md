# Simulação de uso da Fábrica de Software

Você conseguiria conduzir os dois ciclos principais com **quatro prompts essenciais**: um para configurar o repositório, um para implementar a primeira versão e um para cada resultado que precisar de aprovação. A nova feature repetiria o mesmo ciclo: pedido de desenvolvimento e aprovação do resultado.

Os prompts adicionais abaixo cobrem situações que podem surgir — dúvidas, correções, checkpoints, interrupções e cancelamento. Eles não precisam ser usados em sequência se o agente não encontrar esses casos.

A simulação parte destas premissas:

- O novo projeto já existe no GitHub e será desenvolvido em outra pasta, por exemplo `/home/dever/workspace/teknolista/chutegpt-novo`.
- O ambiente de codificação é o **Codex**. Em outro host, mudam os identificadores de instalação e os nomes pelos quais os agentes são descobertos.
- A especificação do ChuteGPT atual será **material de referência**, não prova de que o novo aplicativo está implementado ou testado.
- O conteúdo de [PRODUCT do ChuteGPT](https://github.com/teknolista/chutegpt/blob/main/pentapro/product/overview.md) descreve uma aplicação de terminal para resultados históricos do Dia de Sorte, com **22 análises**. A geração de jogos, pontuação de candidatos e simulação estão explicitamente fora da primeira versão e serão tratadas como uma nova change.
- A especificação também aponta para documentos fora de `pentapro/`, por exemplo referências em `docs/`. Na simulação, o agente precisa localizar essas dependências e perguntar quando o conteúdo necessário não estiver acessível; copiar somente a pasta `pentapro/` pode deixar referências incompletas.

## 1. Preparar o repositório e disponibilizar o PentaPRO

### Passo 1 — Abrir o projeto correto

O desenvolvedor abre no Codex o clone do repositório novo. Para evitar que o agente confunda a pasta da coleção de skills com a pasta da aplicação, o primeiro prompt pode informar os dois caminhos:

> O projeto que iremos desenvolver está em `/home/dever/workspace/teknolista/chutegpt-novo`. Ele já está versionado no GitHub.
>
> Quero usar a coleção PentaPRO e sua fábrica de software neste projeto. Verifique o estado do repositório, a branch, o remoto e as instruções existentes. Depois, disponibilize as skills da coleção no escopo deste projeto e configure a fábrica para Codex.
>
> Não faça commit nem push nesta etapa. Preserve arquivos e configurações existentes e me informe as decisões que precisarem de minha escolha.

**O que a fábrica deve fazer:** verificar o destino, as instalações existentes e as permissões; disponibilizar as skills e executar o setup no projeto correto. Se houver README, licença, tracker ou agentes existentes, deve preservá-los e pedir apenas as escolhas relevantes.

Como alternativa, se o desenvolvedor preferir instalar as skills manualmente no terminal antes de abrir o Codex, a coleção documenta o uso do instalador de skills. A instalação precisa ser feita **no diretório do projeto novo**, não no diretório `skills`. Depois, o desenvolvedor pode solicitar o setup:

> Use `$setup-pentapro` para configurar este repositório com a coleção e a fábrica PentaPRO para Codex.
>
> O projeto será uma nova aplicação de terminal baseada na especificação do ChuteGPT. Configure os arquivos e agentes no escopo do projeto, preserve qualquer conteúdo existente e não publique alterações ainda.

### Decisões que podem ser solicitadas

O setup atual prevê perguntas sobre:

- Tratamento de README existente: **complementar, substituir ou manter**.
- Idioma do README.
- Licença, se o projeto ainda não tiver uma.
- Ambiente efetivamente usado e eventuais ferramentas indisponíveis.

Essas perguntas fazem parte da configuração. O agente deve continuar as partes independentes enquanto espera as respostas.

### Passo 2 — Primeiro checkpoint Git, se desejado

Depois de revisar os arquivos criados pelo setup:

> Acione o agente `factory_shipper` para revisar as alterações de configuração do PentaPRO, criar um commit e fazer push normal para a branch atual.
>
> Inclua apenas os arquivos relacionados à configuração que acabamos de revisar. Preserve quaisquer outras alterações locais.

Esse prompt é opcional. Ele produz um checkpoint de configuração; a implementação da aplicação virá depois.

O `factory_shipper` deve revisar o conjunto exato, executar os checks aplicáveis, criar o commit, fazer o push e confirmar a referência remota. Não deve incluir `AGENTS.log`, arquivos ignorados ou alterações alheias.

---

## 2. Usar a especificação existente sem confundir os projetos

A especificação de origem contém decisões, registros de implementação e evidências do **ChuteGPT original**. Para o projeto novo, a fábrica deve aproveitar os requisitos e decisões aplicáveis, mas registrar que as evidências antigas dizem respeito ao projeto original.

### Passo 3 — Solicitar a implementação inicial

Este é o prompt principal. Ele já pede exploração, especificação, implementação, verificação e revisão; não é necessário chamar cada subagente manualmente.

> Use `$software-factory` para desenvolver a primeira versão deste projeto.
>
> Use como referência a especificação em `/home/dever/workspace/teknolista/chutegpt/pentapro` e os documentos locais aos quais ela faz referência. O projeto de destino é este repositório; não altere o ChuteGPT original.
>
> Quero reproduzir o escopo da primeira versão descrita naquela especificação: aplicação de terminal em português para carregar uma planilha local de resultados do Dia de Sorte e executar as 22 análises históricas especificadas, com navegação, apresentação dos resultados, tratamento de erros, progresso e cancelamento quando aplicáveis.
>
> Preserve as decisões sobre regras numéricas e exemplos de verificação, mas trate os resultados de testes do projeto original apenas como referência histórica. Verifique se os documentos de apoio e os dados necessários estão acessíveis e me pergunte quando faltar uma decisão ou um recurso indispensável.
>
> A geração de palpites, pontuação de candidatos e simulações não fazem parte desta primeira change.
>
> Crie a change nativa PentaPRO, detalhe as cinco dimensões, solicite a revisão da especificação e depois planeje e implemente o trabalho. Acione os especialistas necessários, execute os testes e faça a revisão independente do resultado.
>
> Ao terminar, apresente o aplicativo, as verificações executadas e as limitações para minha validação. Aguarde minha aprovação antes da consolidação e do arquivamento. Após minha aprovação, você poderá fazer commit e push normal da change.

Um nome possível seria:

```text
pentapro/changes/implementacao-inicial/
```

A change conteria:

```text
implementacao-inicial/
├── change.md
├── product.md
├── project.md
├── production.md
├── proof.md
└── process.md
```

O agente escolhe um nome único com duas ou três palavras em minúsculas, separadas por hífens. Ele deve verificar se o nome já está em uso.

### O que aconteceria depois desse prompt

| Etapa | Responsável principal | Ação esperada |
| --- | --- | --- |
| Exploração | Sessão principal/orquestrador | Lê a referência, identifica lacunas e conversa com o desenvolvedor |
| Especificação | `penta-pro` | Registra a change nas cinco dimensões |
| Revisão da especificação | `factory_spec` | Verifica requisitos, cenários, riscos e critérios antes da implementação |
| Planejamento e implementação | `factory_implementer` e `software-delivery` | Divide o trabalho e implementa incrementos verificáveis |
| Testes | Especialistas adequados ao projeto | Executam testes numéricos, de leitura de dados, terminal e integração |
| Verificação | `factory_verifier` | Compara critérios com evidências do novo projeto |
| Revisão | `factory_reviewer` | Procura defeitos e inconsistências no snapshot integrado |
| Correções | Implementador e revisores | Corrigem achados e repetem os checks afetados |
| Validação final | Desenvolvedor | Examina o resultado e decide se o aceita |

**O desenvolvedor não precisa enviar um prompt para cada linha da tabela.** A intenção da fábrica é que o orquestrador faça essas passagens.

### Um ponto a decidir durante a exploração

A especificação original usa uma planilha local e também documenta uma rotina separada de atualização dos resultados. O prompt acima pede a aplicação que lê uma planilha; ele não detalha se o novo projeto deve também possuir o atualizador automático.

O agente deve identificar essa dúvida. Uma resposta possível seria:

> Inclua também um atualizador manual dos resultados oficiais, seguindo o contrato documentado no projeto de referência. O aplicativo continuará lendo uma cópia local; não configure uma tarefa em segundo plano.

Ou:

> Nesta primeira versão, use apenas uma planilha fornecida localmente. A atualização automática fica para outra change.

A autorização permanente que você concedeu para o atualizador do **ChuteGPT original** não deve ser automaticamente transportada para um novo projeto. Na simulação, você pode conceder a mesma autorização explicitamente se quiser.

### Passo 4 — Aprovar a primeira versão

Quando o agente apresentar o resultado e você estiver satisfeito:

> A primeira versão está aprovada. Pode consolidar a especificação nos cinco pilares, arquivar a change e publicar o resultado na branch atual com commit e push normal.

A aprovação libera a sequência padrão:

1. Consolidar os requisitos aceitos nos cinco pilares de `pentapro/`.
2. Arquivar a change com a data local:

   ```text
   pentapro/changes/archive/AAAA-MM-DD_implementacao-inicial/
   ```

3. Acionar `factory_shipper`.
4. Criar o commit, fazer push e confirmar o commit no remoto.
5. Verificar o CI aplicável e informar as limitações.
6. Realizar a retrospectiva do trabalho.

Se você desejar validar o resultado **sem autorizar a publicação**, pode restringir o pedido:

> O resultado funcional está aprovado. Consolide a especificação e arquive a change, mas não faça commit nem push. Quero revisar os arquivos antes da publicação.

Nesse caso, a restrição explícita prevalece sobre o padrão de aprovação única.

---

## 3. Cenário de correção antes da aprovação

Se a primeira implementação não atender ao que você esperava, não é necessário aprová-la. Basta explicar o problema ao orquestrador:

> Ainda não aprovo a primeira versão. Ao abrir a análise de frequência, o aplicativo apresenta valores diferentes dos exemplos da especificação.
>
> Investigue a diferença, corrija o que for necessário, atualize os testes e peça nova verificação e revisão. Preserve as demais análises e me apresente novamente o resultado.

O comportamento esperado é:

1. O agente identifica se há erro no código, na interpretação da regra ou no próprio exemplo.
2. Se a decisão de produto estiver ambígua, pergunta ao desenvolvedor.
3. O implementador corrige o problema.
4. Os checks e as revisões afetados são repetidos.
5. O resultado volta para sua validação.

A aprovação continua pendente enquanto o problema não estiver resolvido ou não houver uma decisão explícita sobre ele.

---

## 4. Fazer checkpoints durante uma implementação longa

A aprovação final da change e os commits intermediários são coisas diferentes. Se você quiser commits periódicos antes do encerramento, pode autorizá-los sem declarar que a feature está aceita:

> Acione o `factory_shipper` para revisar o progresso atual desta change, criar um commit de checkpoint e fazer push normal da branch.
>
> A change continua em andamento. Não a arquive nem apresente este checkpoint como aprovação da funcionalidade.

Esse cenário é especialmente útil se as 22 análises forem implementadas em vários incrementos.

O commit deve representar um estado coerente e revisado. Se houver um teste obrigatório falhando ou um risco de publicar conteúdo sensível, o shipper deve interromper a entrega e explicar o problema.

Para um checkpoint apenas local:

> Acione o `factory_shipper` para criar um commit local do progresso revisado. Não faça push.

Quando chegar o momento de enviar:

> Acione o `factory_shipper` para revisar os commits locais pendentes e fazer push normal da branch atual.

---

## 5. Acrescentar a feature de geração de palpites

Depois de concluída a primeira versão, você pode iniciar uma nova change com um único prompt principal:

> Use `$software-factory` para desenvolver uma nova feature de geração de palpites para o Dia de Sorte.
>
> A aplicação já possui a análise histórica. Quero que o usuário consiga gerar jogos válidos pela interface de terminal, visualizar os números e o mês da sorte e gerar novamente quando desejar.
>
> Antes de implementar, explore comigo as decisões que ainda não estão definidas: como os números e o mês serão escolhidos, se o usuário poderá selecionar critérios, quantos jogos poderão ser gerados e como evitar jogos inválidos ou duplicados.
>
> Preserve as 22 análises existentes e a especificação consolidada. Crie uma nova change PentaPRO, detalhe os requisitos nas cinco dimensões, revise a especificação, implemente, teste e faça a revisão independente.
>
> Não apresente os palpites como previsão garantida nem afirme vantagem estatística sem evidências. Não implemente compras, registro automático de apostas, pagamentos ou integração para apostar.
>
> Ao final, apresente o resultado para minha validação. Após minha aprovação, consolide a especificação, arquive a change e faça commit e push normal.

Um nome possível seria:

```text
pentapro/changes/gerar-palpites/
```

### Perguntas que o agente provavelmente fará

A especificação atual **não define o algoritmo de geração**, então seria inadequado o agente inventar uma estratégia e apresentá-la como uma decisão já tomada.

Perguntas razoáveis incluem:

1. Os jogos serão gerados aleatoriamente ou com filtros baseados nas análises históricas?
2. O usuário poderá escolher quais filtros usar?
3. Quantos jogos poderão ser gerados por vez?
4. Jogos repetidos serão permitidos entre gerações diferentes?
5. O mês da sorte será aleatório, escolhido pelo usuário ou definido por outro critério?
6. Será necessário salvar, exportar ou apenas exibir os palpites?
7. Como o aplicativo deve agir quando os filtros forem tão restritivos que não seja possível gerar a quantidade solicitada?
8. Quais regras vigentes da modalidade precisam ser confirmadas em fonte oficial antes da implementação?

Essas são **questões de produto e contrato**, não respostas implícitas. O agente deve confirmar as regras atuais da modalidade antes de prometer que um jogo é válido.

### Como a change afetaria as cinco dimensões

| Dimensão | Exemplos do que registrar |
| --- | --- |
| **PRODUCT** | Jornada de geração, entradas, jogos válidos, duplicidade, erros e linguagem das mensagens |
| **PROJECT** | Algoritmo escolhido, fonte de aleatoriedade, filtros, limites e integração com as análises |
| **PRODUCTION** | Dados necessários, compatibilidade, instalação, uso offline e tratamento de mudanças nas regras |
| **PROOF** | Casos de validade, repetição, limites, filtros impossíveis e verificações executadas |
| **PROCESS** | Tarefas, responsáveis, decisões pendentes, revisão, aprovação e publicação |

A seleção baseada em resultados históricos pode ser uma funcionalidade legítima de exploração, mas **não demonstra capacidade de prever sorteios futuros**. O aplicativo e sua documentação devem manter essa distinção.

### Aprovação da feature

> Aprovo a feature de geração de palpites conforme apresentada. Pode consolidar a especificação, arquivar a change e fazer commit e push normal.

A nova baseline passaria então a descrever tanto as análises existentes quanto a geração aprovada. A primeira change continuaria no archive como histórico.

---

## 6. Cenário: nova análise, correção ou alteração menor

Para uma nova análise histórica:

> Use `$software-factory` para acrescentar uma análise de distribuição dos intervalos entre sorteios. Preserve as análises atuais, explore as regras necessárias, especifique a change, implemente e verifique. Apresente o resultado para minha aprovação.

Para um defeito específico e bem delimitado:

> Corrija o erro em que o aplicativo não restaura o terminal após interromper uma análise. Preserve a navegação existente, acrescente uma verificação que reproduza o problema e mostre os resultados.

Nesse segundo caso, o orquestrador pode escolher um caminho proporcional. Não deveria iniciar todos os agentes e gerar documentação extensa apenas porque uma alteração pequena foi solicitada, salvo se o projeto exigir esse processo.

Para uma falha intermitente sem causa conhecida:

> Investigue por que a leitura da planilha às vezes falha após a atualização dos resultados. Não presuma a causa. Reproduza o problema quando possível, proponha a correção e, se houver evidência suficiente, implemente e verifique a solução.

Aqui pode ser útil `diagnose-defect`, seguido da skill de implementação adequada e de revisão.

---

## 7. Cenário: pedido apenas de exploração

Se você ainda estiver decidindo como gerar jogos:

> Quero estudar alternativas para geração de palpites no aplicativo. Use `$penta-pro` para explorar possibilidades, riscos e critérios de escolha comigo.
>
> Por enquanto, não implemente, não crie commit e não publique. Apresente opções e suas limitações.

Esse pedido autoriza exploração. Ele **não deve ser interpretado como autorização para começar a implementar**.

Depois que você decidir seguir:

> Vamos implementar a alternativa que discutimos. Use `$software-factory` para abrir a change, revisar a especificação e conduzir implementação, testes e revisão até o ponto da minha validação.

---

## 8. Cenário: solicitar uma revisão independente

Se quiser revisar uma change antes de aceitá-la:

> Acione o `factory_reviewer` para revisar a implementação da change `gerar-palpites` contra seus requisitos e testes.
>
> Faça uma revisão somente de leitura. Apresente defeitos comprovados, riscos e limites de cobertura; não altere os arquivos.

Para uma revisão de segurança específica:

> Use `$cybersec` para avaliar a feature de geração e exportação de palpites, considerando entradas inválidas, exposição de arquivos e dados sensíveis. Faça apenas a análise e apresente os achados.

Esses pedidos são úteis para avaliações adicionais. Eles não aprovam automaticamente o resultado nem autorizam alterações ou publicação.

---

## 9. Cenário: interromper e retomar o trabalho

Se a conversa for interrompida no meio da implementação:

> Retome a change `gerar-palpites` de onde parou.
>
> Antes de continuar, confira o estado real dos arquivos, das tarefas, dos testes e dos efeitos externos já realizados. Preserve alterações locais e continue apenas as etapas ainda necessárias.

A fábrica deve ler os registros atuais, identificar tarefas pendentes e verificar se as evidências ainda correspondem à versão do código. Ela não deve repetir cegamente um commit, push ou arquivamento que possa ter sido concluído antes da interrupção.

Se a publicação falhar por rede ou autenticação:

> Retome a publicação da change `gerar-palpites`. Primeiro confirme o estado do commit local e da branch remota; faça somente a operação que ainda estiver pendente.

---

## 10. Cenário: duas changes afetam o mesmo comportamento

Imagine que uma change altera filtros e outra altera geração de jogos:

> Temos as changes `filtrar-resultados` e `gerar-palpites`. Avalie se elas afetam os mesmos requisitos, arquivos ou contratos.
>
> Coordene a implementação preservando as duas intenções. Se houver conflito material entre decisões, apresente-o antes de consolidar qualquer uma.

A expectativa é que o orquestrador:

- Identifique sobreposição de requisitos e arquivos.
- Evite escritas concorrentes nos mesmos arquivos.
- Reavalie a segunda change se a baseline tiver sido alterada pela primeira.
- Preserve as decisões aceitas em vez de substituir silenciosamente uma pela outra.

---

## 11. Cenário: cancelar uma change

> Quero cancelar a change `gerar-palpites`.
>
> Examine o que já foi implementado e testado, registre os efeitos parciais e apresente as opções para manter ou desfazer o trabalho. Não reverta arquivos automaticamente.

Se você decidir que o código parcial deve ser removido:

> Pode desfazer somente as alterações identificadas como pertencentes à change `gerar-palpites`, preservando qualquer outro trabalho. Depois registre o cancelamento e arquive a change como cancelada.

O archive deve registrar a disposição como **cancelada**, não como uma feature concluída. Se ainda houver efeitos parciais sem decisão, a fábrica deve mantê-los visíveis e resolver a situação antes de dar o cancelamento como encerrado.

---

## 12. Sequência mínima para os dois ciclos

Para visualizar apenas os prompts indispensáveis, supondo que não haja dúvidas adicionais:

| Ordem | Prompt resumido | Resultado |
| --- | --- | --- |
| 1 | “Configure este repositório com `$setup-pentapro` para Codex.” | Skills, instruções e agentes preparados |
| 2 | “Acione `factory_shipper` para commitar e publicar a configuração.” | Checkpoint opcional no GitHub |
| 3 | “Use `$software-factory` para implementar a primeira versão com base na especificação do ChuteGPT.” | Change implementada e apresentada para validação |
| 4 | “Aprovo. Consolide, arquive e publique.” | Primeira versão consolidada e enviada |
| 5 | “Use `$software-factory` para desenvolver a geração de palpites; explore comigo as decisões necessárias.” | Nova change implementada e apresentada |
| 6 | “Aprovo. Consolide, arquive e publique.” | Feature consolidada e enviada |

**O passo 2 é opcional**, assim como checkpoints intermediários. Perguntas de produto podem acrescentar interações nos passos 3 e 5, pois a fábrica não deve inventar decisões importantes.

Há uma limitação prática a validar no ambiente real: os perfis precisam ser descobertos pelo host, e a sessão principal precisa ter capacidade de delegar. Os arquivos e testes atuais descrevem o fluxo pretendido; eles não comprovam que todo host executará autonomamente todos esses passos. Esta resposta é uma **simulação baseada nos contratos atuais**, não uma execução real da fábrica.
