"""Demonstração manual do GerenciadorTarefa (sem frameworks de testes).

Execute a partir da raiz do projeto:
    python -m testes.test_gerenciador_tarefa
"""

from datetime import date, timedelta

from package.gerenciador_tarefa import GerenciadorTarefa
from package.lista import Lista
from package.prioridade import Prioridade
from package.tarefa_simples import TarefaSimples


def separar(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def mostrar_tarefas(lista):
    tarefas = lista.tarefas
    if not tarefas:
        print("A lista está vazia.")
        return

    for tarefa in tarefas:
        status = "Concluída" if tarefa._concluida else "Pendente"
        print(
            f"ID: {tarefa.id} | Título: {tarefa._titulo} | "
            f"Prioridade: {tarefa.prioridade.name} | Status: {status}"
        )


def mostrar_resultado(condicao, descricao):
    print(f"{'OK' if condicao else 'FALHA'}: {descricao}")


def esperar_erro(tipo_erro, acao):
    try:
        acao()
    except tipo_erro as erro:
        print(f"OK - Erro esperado ({tipo_erro.__name__}): {erro}")
    except Exception as erro:
        print(f"FALHA - Erro inesperado ({type(erro).__name__}): {erro}")
    else:
        print(f"FALHA - Era esperado {tipo_erro.__name__}, mas nenhum erro ocorreu.")


def criar_tarefa(identificador, titulo, prioridade=Prioridade.MEDIA):
    return TarefaSimples(
        identificador,
        titulo,
        f"Descrição de {titulo}",
        prioridade,
        date.today() + timedelta(days=10),
    )


def main():
    separar("TESTE 1 - CRIANDO LISTA E GERENCIADOR")
    lista = Lista("Estudos")
    gerenciador = GerenciadorTarefa(lista)
    print("Gerenciador criado para a lista 'Estudos'.")

    separar("TESTE 2 - CONSTRUTOR COM ARGUMENTO INVÁLIDO")
    esperar_erro(TypeError, lambda: GerenciadorTarefa("não é uma lista"))

    separar("TESTE 3 - CRIANDO TAREFAS PELO GERENCIADOR")
    tarefa1 = criar_tarefa(1, "Estudar Python", Prioridade.ALTA)
    tarefa2 = criar_tarefa(2, "Estudar SQL", Prioridade.MEDIA)
    tarefa3 = criar_tarefa(3, "Estudar Git", Prioridade.ALTA)
    tarefa4 = criar_tarefa(4, "Organizar anotações", Prioridade.BAIXA)
    for tarefa in (tarefa1, tarefa2, tarefa3, tarefa4):
        gerenciador.criar(tarefa)
    mostrar_tarefas(lista)
    mostrar_resultado(len(lista.tarefas) == 4, "Quatro tarefas cadastradas")

    separar("TESTE 4 - TENTANDO CADASTRAR ID DUPLICADO")
    duplicada = criar_tarefa(2, "Outra tarefa com ID 2", Prioridade.ALTA)
    esperar_erro(ValueError, lambda: gerenciador.criar(duplicada))
    mostrar_resultado(len(lista.tarefas) == 4, "A lista não foi alterada")

    separar("TESTE 5 - TENTANDO CRIAR OBJETO INVÁLIDO")
    esperar_erro(TypeError, lambda: gerenciador.criar(123))

    separar("TESTE 6 - EDITANDO UMA TAREFA EXISTENTE")
    nova_data = date.today() + timedelta(days=20)
    resultado_edicao = gerenciador.editar(
        tarefa1,
        "Estudar Python avançado",
        "Revisar classes, herança e propriedades",
        nova_data,
    )
    print("Título atualizado:", resultado_edicao._titulo)
    print("Descrição atualizada:", resultado_edicao._descricao)
    print("Nova data:", resultado_edicao._data_vencimento)
    mostrar_resultado(
        tarefa1._titulo == "Estudar Python avançado"
        and tarefa1._descricao == "Revisar classes, herança e propriedades"
        and tarefa1._data_vencimento == nova_data,
        "Dados da tarefa foram atualizados",
    )

    separar("TESTE 7 - EDITANDO ID INEXISTENTE")
    inexistente = criar_tarefa(99, "Não cadastrada")
    esperar_erro(
        ValueError,
        lambda: gerenciador.editar(
            inexistente, "Novo título", "Nova descrição", nova_data
        ),
    )

    separar("TESTE 8 - EDITANDO COM TÍTULO VAZIO")
    esperar_erro(
        ValueError,
        lambda: gerenciador.editar(tarefa2, "   ", "Descrição", nova_data),
    )

    separar("TESTE 9 - CONCLUINDO UMA TAREFA")
    tarefa_concluida = gerenciador.concluir(tarefa2)
    mostrar_resultado(tarefa2._concluida, "Tarefa marcada como concluída")
    print("ID retornado:", tarefa_concluida.id)
    mostrar_tarefas(lista)

    separar("TESTE 10 - CONCLUINDO ID INEXISTENTE")
    esperar_erro(ValueError, lambda: gerenciador.concluir(inexistente))

    separar("TESTE 11 - FILTRANDO TAREFAS POR PRIORIDADE")
    for prioridade in (Prioridade.ALTA, Prioridade.MEDIA, Prioridade.BAIXA):
        encontradas = gerenciador.filtrar(prioridade)
        print(f"\nPrioridade {prioridade.name}: {len(encontradas)} tarefa(s)")
        for tarefa in encontradas:
            print(f"  ID {tarefa.id} - {tarefa._titulo}")
        mostrar_resultado(
            all(tarefa.prioridade == prioridade for tarefa in encontradas),
            f"Filtro {prioridade.name} contém somente a prioridade solicitada",
        )
    mostrar_resultado(
        len(gerenciador.filtrar(Prioridade.ALTA)) == 2,
        "Duas tarefas de prioridade ALTA encontradas",
    )

    separar("TESTE 12 - FILTRO COM TIPO INVÁLIDO")
    esperar_erro(TypeError, lambda: gerenciador.filtrar("ALTA"))

    separar("TESTE 13 - EXCLUINDO TAREFA EXISTENTE")
    gerenciador.excluir(tarefa3)
    mostrar_tarefas(lista)
    mostrar_resultado(
        all(tarefa.id != 3 for tarefa in lista.tarefas),
        "Tarefa com ID 3 removida",
    )

    separar("TESTE 14 - EXCLUINDO COM OUTRA INSTÂNCIA DO MESMO ID")
    outra_instancia = criar_tarefa(4, "Título diferente")
    gerenciador.excluir(outra_instancia)
    mostrar_resultado(
        all(tarefa.id != 4 for tarefa in lista.tarefas),
        "A exclusão foi feita pelo ID, mesmo com outro objeto",
    )

    separar("TESTE 15 - EXCLUINDO TAREFA INEXISTENTE")
    esperar_erro(ValueError, lambda: gerenciador.excluir(inexistente))

    separar("TESTE 16 - PARÂMETROS INVÁLIDOS NOS MÉTODOS")
    esperar_erro(TypeError, lambda: gerenciador.editar("inválido", "A", "B", nova_data))
    esperar_erro(TypeError, lambda: gerenciador.concluir("inválido"))
    esperar_erro(TypeError, lambda: gerenciador.excluir("inválido"))

    separar("TESTE 17 - FILTRO SEM RESULTADOS")
    # Uma lista nova começa vazia: qualquer prioridade deve retornar [].
    gerenciador_vazio = GerenciadorTarefa(Lista("Vazia"))
    resultado_vazio = gerenciador_vazio.filtrar(Prioridade.ALTA)
    print("Resultado:", resultado_vazio)
    mostrar_resultado(resultado_vazio == [], "Lista vazia retornada corretamente")

    separar("ESTADO FINAL DA LISTA")
    mostrar_tarefas(lista)
    print("\nFim da demonstração!")


if __name__ == "__main__":
    main()

