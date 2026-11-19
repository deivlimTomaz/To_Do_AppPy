
# To-Do App Python

Aplicação de gerenciamento de tarefas desenvolvida em **Python**, utilizando conceitos de Programação Orientada a Objetos (POO), persistência com **SQLite** e serialização de objetos em **JSON**.

O sistema funciona pelo terminal e permite organizar tarefas com diferentes comportamentos e prioridades.

## Funcionalidades

- Criar, listar, editar e excluir tarefas.
- Concluir e reabrir tarefas.
- Filtrar tarefas por prioridade: baixa, média e alta.
- Gerenciar tarefas simples, checklists e recorrências.
- Armazenar tarefas em um banco SQLite.
- Preservar os dados após encerrar o aplicativo.
- Serializar e desserializar objetos em JSON.

### Tipos de tarefa

| Tipo | Descrição |
|------|-----------|
| `TarefaSimples` | Tarefa com informações básicas e controle de conclusão. |
| `TarefaChecklist` | Tarefa composta por itens que podem ser adicionados, removidos, marcados e desmarcados. |
| `TarefaRecorr` | Tarefa que permite gerar próximas ocorrências com frequências diária, semanal, mensal ou anual. |

Uma tarefa checklist só pode ser concluída quando todos os seus itens estiverem marcados.

Uma nova ocorrência recorrente só pode ser gerada quando a ocorrência original estiver concluída.

## Tecnologias

- **Python 3**
- **SQLite 3** (`sqlite3`)
- **JSON** (`json`)
- **python-dateutil**
- **Programação Orientada a Objetos**

## Conceitos de POO aplicados

### Abstração

A classe abstrata `Tarefa` define atributos e comportamentos comuns às tarefas.

A classe abstrata `Repositorio` estabelece o contrato para as operações de persistência.

### Herança

As classes `TarefaSimples`, `TarefaChecklist` e `TarefaRecorr` herdam de `Tarefa`.

### Polimorfismo

As subclasses implementam comportamentos específicos, como o método `concluir()`.

### Encapsulamento

Os atributos internos das classes são protegidos e acessados por propriedades e métodos específicos.

### Composição

- `TarefaChecklist` possui objetos `ItemChecklist`.
- `TarefaRecorr` possui um objeto `Recorrencia`.

## Arquitetura

O projeto separa as responsabilidades em três camadas principais:

```text
Menu
  |
  v
GerenciadorTarefa
  |
  v
Repositorio (ABC)
  ^
  |
RepositorioSQLite
  |
  v
SQLite
```

### Componentes principais

| Componente | Responsabilidade |
|------------|------------------|
| `Menu` | Interface de interação pelo terminal. |
| `GerenciadorTarefa` | Regras de negócio e gerenciamento das tarefas. |
| `Tarefa` | Classe abstrata base das tarefas. |
| `Repositorio` | Interface abstrata para operações CRUD. |
| `RepositorioSQLite` | Persistência dos objetos no banco de dados. |
| `RepositorioJson` | Leitura e escrita de arquivos JSON. |
| `fabrica_tarefa` | Reconstrução das subclasses a partir de dicionários. |

## Banco de dados SQLite

O SQLite é utilizado como armazenamento principal do aplicativo.

O banco possui três tabelas:

| Tabela | Descrição |
|--------|-----------|
| `tarefas` | Armazena os atributos comuns das tarefas. |
| `itens_checklist` | Armazena os itens associados aos checklists. |
| `recorrencias` | Armazena as configurações das tarefas recorrentes. |

### Características

- Geração automática de identificadores.
- Relacionamentos com chaves estrangeiras.
- Exclusão em cascata (`ON DELETE CASCADE`).
- Transações com `commit()` e `rollback()`.
- Recuperação de objetos a partir dos registros SQL.

O arquivo `schema.sql` define a estrutura das tabelas.

## Serialização e desserialização JSON

O projeto também implementa a conversão de objetos para JSON e sua reconstrução.

Os métodos utilizados incluem:

- `para_dict()`: converte uma tarefa para dicionário.
- `de_dict()`: reconstrói objetos a partir de dicionários.
- `tarefa_de_dict()`: identifica a subclasse a ser reconstruída.
- `RepositorioJson.salvar()`: grava dados em JSON.
- `RepositorioJson.carregar()`: lê dados de arquivos JSON.

A importação e a exportação são executadas por métodos do gerenciador e verificadas por testes automatizados.

**O SQLite é o armazenamento principal. O JSON é um mecanismo adicional de serialização e transferência de dados.**

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
cd to_do_app
```

Substitua `URL_DO_SEU_REPOSITORIO` pelo endereço do repositório no GitHub.

### 2. Instalar a dependência

```bash
python3 -m pip install python-dateutil
```

### 3. Executar o aplicativo

```bash
python3 main.py
```

Na primeira execução, o programa inicializa as tabelas do SQLite utilizando o arquivo `schema.sql`.

As tarefas cadastradas permanecem armazenadas nas execuções seguintes.

## Testes

O projeto possui testes de integração para verificar as operações de persistência e gerenciamento de tarefas.

Execute os comandos na raiz do projeto:

```bash
python3 -m tests.test_gerenciador_sqlite
python3 -m tests.test_gerenciador_checklist
python3 -m tests.test_gerenciador_recorrencia
python3 -m tests.test_serializacao_json
```

Os testes verificam:

- Criação e recuperação de tarefas.
- Atualização e exclusão de registros.
- Manipulação de checklists.
- Conclusão e reabertura.
- Geração de novas recorrências.
- Persistência com SQLite.
- Serialização e desserialização JSON.

## Diagrama UML

O diagrama UML documenta a estrutura das classes, os relacionamentos de herança e composição e a arquitetura de persistência utilizada no Nível 3.

## Evolução do projeto

### Nível 1
Implementação inicial do gerenciador de tarefas utilizando os fundamentos da Programação Orientada a Objetos.

### Nível 2
Ampliação do sistema com diferentes tipos de tarefas, checklists e recorrências.

### Nível 3
Refatoração da arquitetura e implementação de:

- Persistência com SQLite.
- Repositório abstrato.
- Operações CRUD.
- Identificadores gerados pelo banco.
- Serialização e desserialização JSON.
- Integração completa com a interface de terminal.
- Testes de persistência e regras de negócio.

## Apresentação

O vídeo de apresentação demonstra a arquitetura do projeto, os conceitos de POO utilizados, a persistência SQLite, a serialização JSON e as principais funcionalidades do sistema.

**Link do vídeo:** adicionar após a publicação.

## Licença

Consulte o arquivo `LICENSE`, caso exista no repositório.
