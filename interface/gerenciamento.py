"""Operações de tarefas simples acionadas pela interface, sem dependência gráfica."""
from datetime import datetime

from interface.cadastro import PRIORIDADES
from package.tarefa_simples import TarefaSimples


def buscar_simples(gerenciador, id_tarefa: int) -> TarefaSimples:
    tarefa = gerenciador.buscar_por_id(id_tarefa)
    if not isinstance(tarefa, TarefaSimples):
        raise TypeError("Esta operação está disponível apenas para tarefas simples.")
    return tarefa


def editar_simples(gerenciador, id_tarefa: int, titulo: str, descricao: str,
                   prioridade: str, vencimento: str) -> TarefaSimples:
    tarefa = buscar_simples(gerenciador, id_tarefa)
    if not titulo.strip():
        raise ValueError("Informe o título da tarefa.")
    try:
        prioridade_enum = PRIORIDADES[prioridade]
    except KeyError as erro:
        raise ValueError("Selecione uma prioridade válida.") from erro
    try:
        data = datetime.strptime(vencimento.strip(), "%d/%m/%Y").date()
    except ValueError as erro:
        raise ValueError("Informe uma data válida no formato DD/MM/AAAA.") from erro

    # O domínio permite editar tarefas concluídas sem reabri-las.
    # A validação da data continua no método Tarefa.editar().
    return gerenciador.editar(tarefa, titulo.strip(), descricao.strip(), prioridade_enum, data)


def alternar_conclusao_simples(gerenciador, id_tarefa: int) -> TarefaSimples:
    tarefa = buscar_simples(gerenciador, id_tarefa)
    return gerenciador.reabrir(tarefa) if tarefa.concluida else gerenciador.concluir(tarefa)


def excluir_simples(gerenciador, id_tarefa: int) -> None:
    tarefa = buscar_simples(gerenciador, id_tarefa)
    gerenciador.excluir(tarefa)