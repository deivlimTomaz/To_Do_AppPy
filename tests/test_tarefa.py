
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
print("ID:", tarefa.id)
print("Título:", tarefa.titulo)
print("Descrição:", tarefa.descricao)
print("Prioridade:", tarefa.prioridade)
print("Vencimento:", tarefa.data_vencimento)
print("Concluída:", tarefa.concluida)

print("\n2. Editando a tarefa...")
tarefa.editar(
    "Estudar herança",
    "Revisar classes abstratas",
    Prioridade.ALTA,
    date.today() + timedelta(days=10)
)

print("Novo título:", tarefa.titulo)
print("Nova descrição:", tarefa.descricao)
print("Novo vencimento:", tarefa.data_vencimento)

print("\n3. Verificando atraso:")
print("Está atrasada?", tarefa.esta_atrasada())

print("\n4. Concluindo a tarefa...")
tarefa.concluir()
print("Concluída:", tarefa.concluida)

print("\n5. Tentando criar uma tarefa com título vazio:")

try:
    TarefaDemonstracao(
        2, "", "Descrição",
        prioridade, date.today()
    )
except ValueError as erro:
    print("Erro esperado:", erro)

print("\n6. Verificando criação com data passada (Desserialização):")

try:
    data_passada = date.today() - timedelta(days=1)
    tarefa_passada = TarefaDemonstracao(
        3, "Tarefa antiga", "Descrição",
        prioridade,
        data_passada
    )
    # Valida se o construtor aceitou a data com sucesso
    assert tarefa_passada.data_vencimento == data_passada
    print("OK - Tarefa aceitou data passada com sucesso no construtor.")
except Exception as erro:
    print("FALHA - Não deveria ter lançado erro ao passar data antiga:", erro)


print("\n=== FIM DA DEMONSTRAÇÃO ===")
