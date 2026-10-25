
from package.tarefa_simples import TarefaSimples
from package.prioridade import Prioridade
from datetime import date, timedelta


print("\n=== DEMONSTRAÇÃO DA TAREFA SIMPLES ===")

tarefa = TarefaSimples(
    1,
    "Fazer exercícios",
    "Resolver exercícios de orientação a objetos",
    list(Prioridade)[0],
    date.today() + timedelta(days=3)
)

print("\n1. Criando tarefa simples:")
print("Título:", tarefa._titulo)
print("Descrição:", tarefa._descricao)
print("Concluída:", tarefa._concluida)

print("\n2. Verificando se está atrasada:")
print("Está atrasada?", tarefa.esta_atrasada())

print("\n3. Editando tarefa simples...")

tarefa.editar(
    "Revisar Python",
    "Estudar herança e polimorfismo",
    date.today() + timedelta(days=7)
)

print("Novo título:", tarefa._titulo)
print("Nova descrição:", tarefa._descricao)

print("\n4. Concluindo a tarefa...")

tarefa.concluir()

print("Concluída:", tarefa._concluida)

print("\n=== FIM DA DEMONSTRAÇÃO ===")

