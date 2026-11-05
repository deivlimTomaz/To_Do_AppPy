from package.tarefa_recorr import TarefaRecorr
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from datetime import date, timedelta

prioridade = list(Prioridade)[0]

print("\n=== DEMONSTRAÇÃO DA TAREFA RECORRENTE ===")

tarefa = TarefaRecorr(
    3,
    "Estudar Python",
    "Praticar programação diariamente",
    prioridade,
    date.today(),
    Recorrencia("diaria", 1)
)

print("\n1. Criando tarefa recorrente diária:")
print("Título:", tarefa._titulo)
print("Frequência:", tarefa._recorrencia.frequencia)
print("Vencimento:", tarefa._data_vencimento)
print("Concluída:", tarefa._concluida)

print("\n2. Tentando gerar próxima ocorrência sem concluir:")

try:
    tarefa.gerar_proxima(4)
except ValueError as erro:
    print("Erro esperado:", erro)
else:
    print("FALHA – era esperado erro ao gerar próxima de tarefa pendente")

print("\n3. Concluindo ocorrência atual...")

tarefa.concluir()

print("Concluída:", tarefa._concluida)

print("\n4. Gerando próxima ocorrência diária...")

proxima = tarefa.gerar_proxima(4)

print("Novo ID:", proxima._id)
print("Título:", proxima._titulo)
print("Novo vencimento:", proxima._data_vencimento)
print("Concluída:", proxima._concluida)

print("\n5. Criando tarefa recorrente semanal...")

semanal = TarefaRecorr(
    5,
    "Revisar conteúdo",
    "Revisão semanal de Python",
    prioridade,
    date.today(),
    Recorrencia("semanal", 1)
)

semanal.concluir()
proxima_semanal = semanal.gerar_proxima(6)

print("Vencimento original:", semanal._data_vencimento)
print("Próximo vencimento:", proxima_semanal._data_vencimento)

print("\n6. Tentando usar frequência inválida:")

try:
    # Criando o objeto Recorrencia dentro do try com valor realmente inválido
    recorrencia_invalida = Recorrencia("quinzenal", 1)
    TarefaRecorr(
        7,
        "Tarefa inválida",
        "Descrição",
        prioridade,
        date.today(),
        recorrencia_invalida
    )
except ValueError as erro:
    print("Erro esperado:", erro)
else:
    print("FALHA – era esperado erro para frequência inválida")

print("\n6b. Tentando usar intervalo inválido (zero ou negativo):")

try:
    recorrencia_intervalo_ruim = Recorrencia("diaria", 0)
except ValueError as erro:
    print("Erro esperado:", erro)
else:
    print("FALHA – era esperado erro para intervalo menor ou igual a zero")

print("\n6c. Tentando passar tipo errado no construtor da TarefaRecorr:")

try:
    # Passando uma string pura onde deveria ser um objeto Recorrencia
    TarefaRecorr(
        7,
        "Tipo Inválido",
        "Descrição",
        prioridade,
        date.today(),
        "diaria"
    )
except TypeError as erro:
    print("Erro esperado:", erro)
else:
    print("FALHA – era esperado TypeError ao passar string no lugar de Recorrencia")

print("\n7. Simulando uma ocorrência atrasada...")

atrasada = TarefaRecorr(
    8,
    "Praticar Python",
    "Exercícios diários",
    prioridade,
    date.today(),
    Recorrencia("diaria", 1)
)

atrasada.concluir()

# Simulando a passagem de vários dias.
atrasada._data_vencimento = date.today() - timedelta(days=10)

nova_ocorrencia = atrasada.gerar_proxima(9)

print("Vencimento anterior:", atrasada._data_vencimento)
print("Próximo vencimento válido:", nova_ocorrencia._data_vencimento)

print("\n=== FIM DA DEMONSTRAÇÃO ===")

