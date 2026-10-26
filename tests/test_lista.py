
from datetime import date, timedelta

from package.lista import Lista
from package.tarefa_simples import TarefaSimples
from package.prioridade import Prioridade


def separar(titulo):
    print("\n" + "=" * 55)
    print(titulo)
    print("=" * 55)


def mostrar_tarefas(lista):
    if not lista._tarefas:
        print("A lista está vazia.")
        return

    for tarefa in lista._tarefas:
        print(f"ID: {tarefa.id} | Título: {tarefa._titulo}")


def main():
    separar("TESTE 1 - CRIANDO UMA LISTA")

    lista = Lista("Estudos")
    print("Lista 'Estudos' criada com sucesso!")


    separar("TESTE 2 - VALIDANDO NOME VAZIO")

    try:
        Lista("   ")
    except ValueError as erro:
        print(f"Erro esperado: {erro}")


    separar("TESTE 3 - CRIANDO TAREFAS")

    tarefa1 = TarefaSimples(
        1,
        "Estudar Python",
        "Revisar orientação a objetos",
        Prioridade.ALTA,
        date.today() + timedelta(days=3)
    )

    tarefa2 = TarefaSimples(
        2,
        "Estudar SQL",
        "Praticar consultas",
        Prioridade.MEDIA,
        date.today() + timedelta(days=5)
    )

    tarefa3 = TarefaSimples(
        3,
        "Estudar Git",
        "Praticar commits",
        Prioridade.BAIXA,
        date.today() + timedelta(days=7)
    )

    print("Três tarefas criadas com sucesso!")


    separar("TESTE 4 - ADICIONANDO TAREFAS")

    lista.adicionar(tarefa1)
    lista.adicionar(tarefa2)
    lista.adicionar(tarefa3)

    mostrar_tarefas(lista)


    separar("TESTE 5 - TENTANDO ADICIONAR ID DUPLICADO")

    tarefa_duplicada = TarefaSimples(
        2,
        "Outra tarefa",
        "Tarefa com ID já cadastrado",
        Prioridade.ALTA,
        date.today() + timedelta(days=10)
    )

    try:
        lista.adicionar(tarefa_duplicada)
        print("FALHA: tarefa duplicada foi adicionada!")
    except ValueError as erro:
        print(f"Erro esperado: {erro}")

    mostrar_tarefas(lista)


    separar("TESTE 6 - ADICIONANDO OBJETO INVÁLIDO")

    try:
        lista.adicionar("Não sou uma tarefa")
        print("FALHA: objeto inválido foi adicionado!")
    except TypeError as erro:
        print(f"Erro esperado: {erro}")


    separar("TESTE 7 - REMOVENDO TAREFA EXISTENTE")

    removida = lista.remover(tarefa2)

    print(f"Tarefa removida: {removida._titulo}")
    mostrar_tarefas(lista)


    separar("TESTE 8 - REMOVENDO TAREFA INEXISTENTE")

    try:
        lista.remover(tarefa2)
        print("FALHA: tarefa inexistente foi removida!")
    except ValueError as erro:
        print(f"Erro esperado: {erro}")


    separar("TESTE 9 - REMOVENDO OBJETO INVÁLIDO")

    try:
        lista.remover(123)
        print("FALHA: objeto inválido foi aceito!")
    except TypeError as erro:
        print(f"Erro esperado: {erro}")


    separar("TESTE 10 - REMOVENDO POR ID")

    # Objeto diferente, mas com o mesmo ID da tarefa1
    outra_instancia = TarefaSimples(
        1,
        "Título diferente",
        "Objeto diferente com ID igual",
        Prioridade.BAIXA,
        date.today() + timedelta(days=2)
    )

    removida = lista.remover(outra_instancia)

    print(f"Tarefa removida pelo ID: {removida._titulo}")
    mostrar_tarefas(lista)


    separar("TESTE 11 - ESVAZIANDO A LISTA")

    lista.remover(tarefa3)

    mostrar_tarefas(lista)


    separar("FIM DOS TESTES")
    print("Demonstração das funcionalidades finalizada!")


if __name__ == "__main__":
    main()

