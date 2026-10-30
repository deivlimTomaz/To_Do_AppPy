# Gerenciador de Tarefas — To-Do App em Python

Projeto acadêmico de **Programação Orientada a Objetos (POO)** desenvolvido em Python. O objetivo é construir um gerenciador de tarefas evolutivo, começando pela modelagem das classes e chegando a um menu interativo, persistência em banco de dados e interface gráfica.

> **Estado atual:** núcleo de classes e demonstração funcional do Nível 1. O menu principal, a interface gráfica e outras funcionalidades planejadas ainda não fazem parte da demonstração atual.

## Funcionalidades implementadas e demonstradas

- Criação e organização de tarefas em **listas** associadas a **categorias**.
- **Tarefa simples:** cadastro e conclusão.
- **Tarefa checklist:** adição e marcação de itens; conclusão condicionada à finalização de todos os itens.
- **Tarefa recorrente:** frequências diária, semanal, mensal e anual, com intervalo configurável; geração de nova ocorrência após a conclusão da anterior.
- **Gerenciamento:** cadastro, edição, conclusão, exclusão e filtragem de tarefas por prioridade.
- **Prioridades:** baixa, média e alta.
- **Serialização:** representação de tarefas em dicionários; há classes com suporte a reconstrução a partir desses dados.
- **Persistência em JSON:** implementação de repositório para salvar e carregar dados, ainda não integrada a um fluxo completo de menu.

## Conceitos de POO utilizados

| Conceito | Aplicação no projeto |
| --- | --- |
| **Abstração** | `Tarefa` define a estrutura comum às tarefas. |
| **Herança** | `TarefaSimples`, `TarefaChecklist` e `TarefaRecorr` derivam de `Tarefa`. |
| **Polimorfismo** | A operação `concluir()` é utilizada para diferentes tipos de tarefa, respeitando as regras de cada um. |
| **Composição** | `TarefaChecklist` gerencia objetos `ItemChecklist`. |
| **Associação** | `Lista` mantém tarefas e referencia uma `Categoria`; uma categoria pode ser compartilhada entre listas. |
| **Dependência** | `GerenciadorTarefa` utiliza o enum `Prioridade` para filtrar tarefas. |
| **Encapsulamento** | Uso de atributos internos e propriedades para acesso controlado aos dados. |

## Estrutura principal

```text
To_Do_AppPy/
├── package/
│   ├── tarefa.py
│   ├── tarefa_simples.py
│   ├── tarefa_checklist.py
│   ├── item_checklist.py
│   ├── tarefa_recorr.py
│   ├── recorrencia.py
│   ├── prioridade.py
│   ├── categoria.py
│   ├── lista.py
│   ├── gerenciador_tarefa.py
│   ├── repositorio.py
│   ├── repositorio_json.py
│   ├── lembrete.py
│   ├── servico_lembrete.py
│   └── notificador.py
├── tests/
├── main.py
└── README.md
```

> A estrutura acima relaciona os arquivos identificados no projeto fornecido. Os arquivos `test_nivel1.py` e `demonstracao_nivel1.py` podem ser adicionados conforme a organização local do projeto. `main.py` ainda não deve ser entendido como um menu completo.

## Requisitos

- Python 3.10 ou superior (recomendado).
- Biblioteca [`python-dateutil`](https://pypi.org/project/python-dateutil/), utilizada no cálculo das recorrências.

Instale a dependência:

```bash
python -m pip install python-dateutil
```

## Como executar a demonstração

A partir da pasta raiz do projeto, com o arquivo `demonstracao_nivel1.py` ao lado da pasta `package`:

```bash
python demonstracao_nivel1.py
```

A demonstração apresenta, no terminal, exemplos de:

1. Criação de listas e associação com categorias.
2. Cadastro dos três tipos de tarefa.
3. Inclusão e marcação de itens de checklist.
4. Conclusão de tarefas com comportamentos diferentes.
5. Geração da próxima ocorrência de tarefa recorrente.
6. Filtragem por prioridade.
7. Edição e exclusão de tarefas.

### Executando o teste de integração

Se o arquivo de teste estiver disponível como `tests/test_nivel1.py`, execute:

```bash
python -m tests.test_nivel1
```

Esse teste valida cenários de funcionamento de forma automatizada. A **demonstração funcional** é um arquivo separado, voltado à apresentação do comportamento das classes. Os testes realizados até agora não garantem cobertura integral de todos os módulos.

## Arquitetura e UML

O sistema separa as responsabilidades de **modelo de domínio**, **gerenciamento** e **persistência**.

- `Tarefa` e subclasses representam o domínio das tarefas.
- `GerenciadorTarefa` coordena operações sobre tarefas de uma `Lista`.
- `Recorrencia` calcula datas e intervalos de repetição.
- `Repositorio` define o contrato de persistência, implementado por `RepositorioJson`.
- `MenuPrincipal` está **planejado** para oferecer interação no terminal por meio de operações de cadastro, consulta, edição e exclusão (CRUD).
- `JanelaPrincipal` está **planejada** para a futura interface gráfica.

O diagrama de classes UML deve ser mantido em sincronia com as classes efetivamente implementadas, distinguindo os elementos ainda planejados.

## Etapas do projeto

| Etapa | Objetivo | Situação |
| --- | --- | --- |
| **Nível 1** | Modelagem UML, relacionamentos de POO e demonstração de funcionalidades | Demonstração integrada executada com sucesso; entrega em preparação |
| **Nível 2** | Menu funcional para acessar os recursos do sistema | Planejado |
| **Nível 3** | Persistência em banco de dados | Planejado |
| **Nível 4** | Interface gráfica personalizada | Planejado |

## Próximos passos

- Implementar `MenuPrincipal` sem misturar entrada/saída do terminal com as regras de negócio.
- Ampliar a cobertura dos testes e revisar a serialização/desserialização das tarefas recorrentes.
- Integrar a persistência ao fluxo da aplicação.
- Evoluir os recursos de lembretes e notificações.
- Implementar a interface gráfica em uma etapa posterior.

## Sobre

Projeto desenvolvido para fins acadêmicos e aprendizado de Python, orientação a objetos, modelagem UML e organização de software em camadas.
