# To-Do App Python

Aplicativo desktop de gerenciamento de tarefas em **Python**, desenvolvido com **Programação Orientada a Objetos (POO)**, interface gráfica **CustomTkinter** e persistência em **SQLite**. A versão de terminal permanece disponível. O projeto também implementa importação e exportação de tarefas em JSON pela camada de gerenciamento.

## Funcionalidades

| Tipo | Funcionalidades |
| --- | --- |
| Tarefa simples | Cadastrar, consultar, editar, concluir, reabrir e excluir. |
| Checklist | Cadastrar, editar dados gerais, adicionar/remover e marcar/desmarcar itens, acompanhar progresso, concluir, reabrir e excluir. |
| Recorrente | Cadastrar, editar dados gerais, frequência e intervalo, concluir, reabrir, gerar a próxima ocorrência e excluir. |

Todas as tarefas possuem título, descrição, prioridade, data de vencimento e estado de conclusão. A interface apresenta seções para **Tarefas** (todos os tipos), **Checklists** e **Recorrentes**, além de botão de atualização e alternância entre **tema claro e escuro**.

### Regras relevantes

- Checklists só podem ser concluídos quando possuem itens e todos estão marcados. Enquanto concluídos, seus itens não podem ser alterados; a reabertura permite editá-los novamente.
- As informações gerais de tarefas concluídas podem ser editadas sem alterar automaticamente seu estado.
- Uma tarefa recorrente pode ter frequência **diária, semanal, mensal ou anual** e intervalo inteiro positivo.
- A próxima ocorrência só pode ser gerada a partir de uma tarefa recorrente concluída. Ela recebe um novo ID e mantém a ocorrência anterior no banco.
- Alterações na configuração de uma ocorrência não atualizam retroativamente ocorrências já cadastradas.
- **Limitação atual:** é possível acionar a geração da próxima ocorrência mais de uma vez na mesma tarefa concluída; não existe bloqueio de duplicatas nessa operação.

## Tecnologias

- Python 3 (testado pelo autor no Linux nativo; requer instalação local compatível com Tkinter)
- CustomTkinter (janelas, botões, campos, estilos e temas)
- Tkinter (dependência gráfica usada pelo CustomTkinter)
- SQLite (`sqlite3`, biblioteca padrão)
- `python-dateutil` (cálculo de recorrências, inclusive mensal e anual)
- JSON (`json`, biblioteca padrão)
- `unittest` (testes automatizados)

## Organização e arquitetura

```text
To_Do_AppPy/
├── main.py                       # Terminal
├── main_gui.py                   # Interface gráfica
├── schema.sql                    # Estrutura SQLite
├── package/                      # Domínio, gerenciamento, repositórios, menu
│   ├── tarefa.py
│   ├── tarefa_simples.py
│   ├── tarefa_checklist.py
│   ├── tarefa_recorr.py
│   ├── item_checklist.py
│   ├── recorrencia.py
│   ├── prioridade.py
│   ├── gerenciador_tarefa.py
│   ├── repositorio.py
│   ├── repositorio_sqlite.py
│   ├── repositorio_json.py
│   ├── fabrica_tarefa.py
│   ├── conexao.py
│   └── menu.py
├── interface/                    # Interface CustomTkinter
│   ├── app.py
│   ├── cadastro.py
│   ├── janela_cadastro.py
│   ├── gerenciamento.py
│   ├── janela_detalhes.py
│   ├── tarefas_view.py
│   ├── checklist_operacoes.py
│   ├── checklist_formulario.py
│   ├── janela_checklist.py
│   ├── janela_formulario_checklist.py
│   ├── recorrencia_operacoes.py
│   ├── janela_formulario_recorr.py
│   └── janela_recorrencia.py
├── tests/                        # Testes dos níveis anteriores e da interface
└── docs/
    ├── uml_nivel4_dominio.mmd
    └── uml_nivel4_interface.mmd
```

### Fluxo de responsabilidades

```text
main_gui.py → App / janelas CustomTkinter
                         ↓
               Operações da interface
                         ↓
                GerenciadorTarefa
                         ↓
                 Repositorio (ABC)
                         ↑
                 RepositorioSQLite
                         ↓
                       SQLite

main.py → Menu (terminal) → GerenciadorTarefa (mesmas regras)
```

A interface é responsável por apresentar formulários, mensagens e controles. As regras de tarefas ficam no domínio e em `GerenciadorTarefa`. O repositório efetua a persistência, sem SQL dentro das janelas.

### Classes principais

| Componente | Responsabilidade |
| --- | --- |
| `Tarefa` | Classe abstrata com os campos e comportamentos comuns. |
| `TarefaSimples` | Tarefa com conclusão direta. |
| `TarefaChecklist` / `ItemChecklist` | Itens e regras de conclusão por checklist. |
| `TarefaRecorr` / `Recorrencia` | Configuração e cálculo de novas ocorrências. |
| `GerenciadorTarefa` | Casos de uso e operações sobre as tarefas; no Nível 4, inclui edição da configuração de recorrência. |
| `Repositorio` / `RepositorioSQLite` | Contrato CRUD e implementação persistente. |
| `RepositorioJson` / `fabrica_tarefa` | Serialização e reconstrução dos tipos de tarefa. |
| `Menu` | Interação via terminal (mantida). |
| `App` | Janela principal, filtros, cartões, navegação e tema. |
| `JanelaCadastro` / `JanelaDetalhes` | Formulário e gerenciamento de tarefas simples. |
| `JanelaFormularioChecklist` / `JanelaChecklist` | Cadastro/edição de dados e gerenciamento de itens de checklist. |
| `JanelaFormularioRecorr` / `JanelaRecorrencia` | Cadastro/edição e gerenciamento de ocorrências recorrentes. |

## Banco de dados

O banco SQLite possui três tabelas: `tarefas`, `itens_checklist` e `recorrencias`. O esquema é definido em `schema.sql`, com IDs gerados pelo SQLite, relacionamentos por chaves estrangeiras e exclusão em cascata. A persistência utiliza transações.

Por padrão, `tarefas.db` é mantido na pasta do projeto e é ignorado pelo Git. Se precisar preservar os dados ao mudar de computador, copie esse arquivo com o aplicativo fechado.

## Instalação e execução (Linux)

Na raiz do projeto:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install customtkinter python-dateutil
python3 main_gui.py
```

Se o sistema não oferecer Tkinter ao Python utilizado, instale o pacote Tk correspondente à sua distribuição. Em distribuições Ubuntu/Debian, normalmente é disponibilizado como `python3-tk`, mas a versão deve corresponder ao interpretador em uso.

Para executar a versão de terminal:

```bash
python3 main.py
```

> Execute os comandos a partir da raiz do projeto. A interface gráfica foi preparada para usar `tarefas.db` no diretório do projeto.

## Testes

Os testes de integração do Nível 4 usam bancos SQLite temporários, sem depender dos dados reais do usuário. Execute na raiz do projeto:

```bash
python3 -m unittest \
  tests.test_interface_integracao \
  tests.test_interface_cadastro \
  tests.test_interface_gerenciamento \
  tests.test_interface_checklist \
  tests.test_interface_formulario_checklist \
  tests.test_interface_recorrencia
```

Para os principais testes anteriores:

```bash
python3 -m tests.test_gerenciador_sqlite
python3 -m tests.test_gerenciador_checklist
python3 -m tests.test_gerenciador_recorrencia
python3 -m tests.test_serializacao_json
```

Teste manualmente a interface no Linux: criação/edição/exclusão dos três tipos, regras de conclusão, geração da próxima ocorrência, alteração de tema e persistência após reiniciar. Os testes automatizados de operações não substituem a validação dos botões e janelas.

## Diagramas UML

Arquivos-fonte em Mermaid, que podem ser importados no draw.io por **Inserir → Avançado → Mermaid**:

- [`docs/uml_nivel4_dominio.mmd`](docs/uml_nivel4_dominio.mmd): domínio, composição, gerenciamento e persistência.
- [`docs/uml_nivel4_interface.mmd`](docs/uml_nivel4_interface.mmd): classes gráficas, módulos de operação e dependências com o gerenciador.

Os diagramas mostram as relações principais, não todos os atributos, métodos auxiliares ou módulos de suporte.

## Evolução do projeto

**Nível 1:** implementação inicial com fundamentos de POO.

**Nível 2:** tarefas simples, checklists e recorrências.

**Nível 3:** arquitetura em camadas, CRUD com SQLite, identificação automática, serialização JSON e testes de persistência.

**Nível 4:** interface desktop com CustomTkinter, temas claro/escuro, navegação por tipo de tarefa, formulários gráficos de cadastro e edição, operações sobre checklists e recorrências, integração com o gerenciador existente e testes específicos de interface/integração.

## Apresentação do Nível 4

O vídeo de até **6 minutos**, publicado no YouTube, demonstrará a interface, os botões e estilos personalizados, as tarefas simples, os checklists, as recorrências e a persistência após reiniciar.

**Link do vídeo:** adicionar após a publicação.

## Licença

Consulte o arquivo `LICENSE`, se estiver presente no repositório.
