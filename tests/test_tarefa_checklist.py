
from package.tarefa_checklist import TarefaChecklist
from package.prioridade import Prioridade
from datetime import date, timedelta


print("\n=== DEMONSTRAÇÃO DA TAREFA CHECKLIST ===")

tarefa = TarefaChecklist(
    2,
    "Preparar apresentação",
    "Apresentação do projeto de POO",
    list(Prioridade)[0],
    date.today() + timedelta(days=5)
)

print("\n1. Criando tarefa checklist:")
print("Título:", tarefa._titulo)
print("Itens iniciais:", tarefa._itens)

print("\n2. Adicionando itens...")

tarefa.adicionar_item("Criar slides")
tarefa.adicionar_item("Revisar código")
tarefa.adicionar_item("Ensaiar apresentação")

for indice, item in enumerate(tarefa._itens):
    print(indice, "-", item["nome"], "| Feito:", item["feito"])

print("\n3. Tentando concluir antes de finalizar os itens:")

try:
    tarefa.concluir()
except ValueError as erro:
    print("Erro esperado:", erro)

print("\n4. Marcando o primeiro item...")

tarefa.marcar_item(0)

print("Itens:", tarefa._itens)
print("Todos feitos?", tarefa.todos_feitos())

print("\n5. Marcando os itens restantes...")

tarefa.marcar_item(1)
tarefa.marcar_item(2)

for item in tarefa._itens:
    print(item["nome"], "| Feito:", item["feito"])

print("Todos feitos?", tarefa.todos_feitos())

print("\n6. Concluindo a tarefa...")

tarefa.concluir()

print("Tarefa concluída:", tarefa._concluida)

print("\n7. Tentando adicionar item após conclusão:")

try:
    tarefa.adicionar_item("Novo item")
except ValueError as erro:
    print("Erro esperado:", erro)

print("\n8. Tentando marcar índice inválido:")

try:
    tarefa.marcar_item(99)
except IndexError as erro:
    print("Erro esperado:", erro)

print("\n=== FIM DA DEMONSTRAÇÃO ===")

