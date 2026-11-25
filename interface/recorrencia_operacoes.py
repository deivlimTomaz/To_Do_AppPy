"""Operações de recorrência utilizadas pela interface gráfica."""

from datetime import datetime

from interface.cadastro import PRIORIDADES

from package.recorrencia import Recorrencia
from package.tarefa_recorr import TarefaRecorr


FREQUENCIAS = {
    "Diária": "diaria",
    "Semanal": "semanal",
    "Mensal": "mensal",
    "Anual": "anual",
}


def buscar_recorrente(gerenciador, id_tarefa):

    tarefa = gerenciador.buscar_por_id(id_tarefa)

    if not isinstance(tarefa, TarefaRecorr):
        raise TypeError(
            "A tarefa não é recorrente."
        )

    return tarefa


def validar_formulario(
    titulo,
    descricao,
    prioridade,
    vencimento,
    frequencia,
    intervalo
):

    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("Informe um título.")

    if not isinstance(descricao, str):
        raise TypeError(
            "A descrição deve ser um texto."
        )

    # Conversão da prioridade e da frequência.

    try:
        prioridade_enum = PRIORIDADES[prioridade]
        frequencia_interna = FREQUENCIAS[frequencia]

    except (KeyError, TypeError) as erro:
        raise ValueError(
            "Prioridade ou frequência inválida."
        ) from erro

    # Conversão da data.

    try:
        data = datetime.strptime(
            vencimento.strip(),
            "%d/%m/%Y"
        ).date()

    except (AttributeError, ValueError) as erro:
        raise ValueError(
            "Data inválida. Use DD/MM/AAAA."
        ) from erro

    # Conversão do intervalo.

    try:
        intervalo_inteiro = int(intervalo.strip())

    except (AttributeError, ValueError) as erro:
        raise ValueError(
            "O intervalo deve ser um inteiro positivo."
        ) from erro

    if intervalo.strip() != str(intervalo_inteiro):
        raise ValueError(
            "O intervalo deve ser um inteiro positivo."
        )

    # O próprio domínio valida frequência e intervalo.
    recorrencia = Recorrencia(
        frequencia_interna,
        intervalo_inteiro
    )

    return (
        titulo.strip(),
        descricao.strip(),
        prioridade_enum,
        data,
        recorrencia
    )


def criar_recorrente(gerenciador, *campos):

    titulo, descricao, prioridade, data, recorrencia = (
        validar_formulario(*campos)
    )

    tarefa = TarefaRecorr(
        None,
        titulo,
        descricao,
        prioridade,
        data,
        recorrencia
    )

    return gerenciador.criar(tarefa)


def editar_recorrente(
    gerenciador,
    id_tarefa,
    *campos
):

    titulo, descricao, prioridade, data, recorrencia = (
        validar_formulario(*campos)
    )

    return gerenciador.editar_recorrente(
        id_tarefa,
        titulo,
        descricao,
        prioridade,
        data,
        recorrencia.frequencia,
        recorrencia.intervalo
    )


def alternar_conclusao(gerenciador, id_tarefa):

    tarefa = buscar_recorrente(
        gerenciador,
        id_tarefa
    )

    if tarefa.concluida:
        return gerenciador.reabrir(tarefa)

    return gerenciador.concluir(tarefa)


def gerar_proxima(gerenciador, id_tarefa):

    buscar_recorrente(
        gerenciador,
        id_tarefa
    )

    return gerenciador.gerar_proxima_recorrencia(
        id_tarefa
    )


def excluir_recorrente(gerenciador, id_tarefa):

    tarefa = buscar_recorrente(
        gerenciador,
        id_tarefa
    )

    gerenciador.excluir(tarefa)