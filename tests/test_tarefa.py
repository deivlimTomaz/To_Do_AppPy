
from package.tarefa import Tarefa
from package.prioridade import Prioridade
from datetime import date, timedelta


class TarefaDemonstracao(Tarefa):
    def concluir(self):
        super().concluir()


prioridade = list(Prioridade)[0]

print("\n=== DEMONSTRAÇÃO DA CLASSE TAREFA ===")

tarefa = TarefaDemonstracao(
    1,
    "Estudar Python",
    "Revisar programação orientada a objetos",
    prioridade,
    date.today() + timedelta(days=5)
)

print("\n1. Tarefa criada:")
print("ID:", tarefa._id)
print("Título:", tarefa._titulo)
print("Descrição:", tarefa._descricao)
print("Prioridade:", tarefa._prioridade)
print("Vencimento:", tarefa._data_vencimento)
print("Concluída:", tarefa._concluida)

print("\n2. Editando a tarefa...")
tarefa.editar(
    "Estudar herança",
    "Revisar classes abstratas",
    date.today() + timedelta(days=10)
)

print("Novo título:", tarefa._titulo)
print("Nova descrição:", tarefa._descricao)
print("Novo vencimento:", tarefa._data_vencimento)

print("\n3. Verificando atraso:")
print("Está atrasada?", tarefa.esta_atrasada())

print("\n4. Concluindo a tarefa...")
tarefa.concluir()
print("Concluída:", tarefa._concluida)

print("\n5. Tentando criar uma tarefa com título vazio:")

try:
    TarefaDemonstracao(
        2, "", "Descrição",
        prioridade, date.today()
    )
except ValueError as erro:
    print("Erro esperado:", erro)

print("\n6. Tentando criar uma tarefa com data passada:")

try:
    TarefaDemonstracao(
        3, "Tarefa inválida", "Descrição",
        prioridade,
        date.today() - timedelta(days=1)
    )
except ValueError as erro:
    print("Erro esperado:", erro)

print("\n=== FIM DA DEMONSTRAÇÃO ===")

