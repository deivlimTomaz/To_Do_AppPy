"""Adaptadores da interface para operações de checklist existentes no domínio."""

from package.tarefa_checklist import TarefaChecklist


def buscar_checklist(gerenciador, id_tarefa):
    tarefa = gerenciador.buscar_por_id(id_tarefa)

    if not isinstance(tarefa, TarefaChecklist):
        raise TypeError(
            "A tarefa selecionada não é um checklist."
        )

    return tarefa


def adicionar_item(gerenciador, id_tarefa, texto):
    buscar_checklist(gerenciador, id_tarefa)

    return gerenciador.adicionar_item(
        id_tarefa,
        texto.strip()
    )


def remover_item(gerenciador, id_tarefa, indice):
    buscar_checklist(gerenciador, id_tarefa)

    return gerenciador.remover_item(
        id_tarefa,
        indice
    )


def alternar_item(gerenciador, id_tarefa, indice):
    tarefa = buscar_checklist(gerenciador, id_tarefa)

    if tarefa.itens[indice].feito:
        return gerenciador.desmarcar_item(
            id_tarefa,
            indice
        )

    return gerenciador.marcar_item(
        id_tarefa,
        indice
    )


def alternar_conclusao(gerenciador, id_tarefa):
    tarefa = buscar_checklist(gerenciador, id_tarefa)

    if tarefa.concluida:
        return gerenciador.reabrir(tarefa)

    return gerenciador.concluir(tarefa)