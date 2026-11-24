"""Conversão dos dados de formulário para operações de checklist."""

from datetime import datetime

from interface.cadastro import PRIORIDADES
from interface.checklist_operacoes import buscar_checklist

from package.tarefa_checklist import TarefaChecklist


def validar_campos(titulo, descricao, prioridade, vencimento):

    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError(
            "Informe o título do checklist."
        )

    if not isinstance(descricao, str):
        raise TypeError(
            "A descrição deve ser um texto."
        )

    try:
        prioridade_enum = PRIORIDADES[prioridade]

    except (KeyError, TypeError) as erro:
        raise ValueError(
            "Selecione uma prioridade válida."
        ) from erro

    try:
        data = datetime.strptime(
            vencimento.strip(),
            "%d/%m/%Y"
        ).date()

    except (ValueError, AttributeError) as erro:
        raise ValueError(
            "Informe uma data válida no formato DD/MM/AAAA."
        ) from erro

    return (
        titulo.strip(),
        descricao.strip(),
        prioridade_enum,
        data
    )


def criar_checklist(
    gerenciador,
    titulo,
    descricao,
    prioridade,
    vencimento
):
    dados = validar_campos(
        titulo,
        descricao,
        prioridade,
        vencimento
    )

    tarefa = TarefaChecklist(
        None,
        *dados
    )

    return gerenciador.criar(tarefa)


def editar_checklist(
    gerenciador,
    id_tarefa,
    titulo,
    descricao,
    prioridade,
    vencimento
):
    tarefa = buscar_checklist(
        gerenciador,
        id_tarefa
    )

    dados = validar_campos(
        titulo,
        descricao,
        prioridade,
        vencimento
    )

    return gerenciador.editar(
        tarefa,
        *dados
    )


def excluir_checklist(gerenciador, id_tarefa):

    tarefa = buscar_checklist(
        gerenciador,
        id_tarefa
    )

    gerenciador.excluir(tarefa)