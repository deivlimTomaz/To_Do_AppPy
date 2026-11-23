"""Preparação dos dados exibidos pela interface, sem dependência gráfica."""

from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr


def filtrar_tarefas(tarefas, secao):
    """Retorna as tarefas pertencentes à seção indicada."""
    if secao == "Tarefas":
        return list(tarefas)
    if secao == "Checklists":
        return [t for t in tarefas if isinstance(t, TarefaChecklist)]
    if secao == "Recorrentes":
        return [t for t in tarefas if isinstance(t, TarefaRecorr)]
    raise ValueError(f"Seção desconhecida: {secao}")


def resumo_tarefa(tarefa):
    """Retorna os campos públicos necessários para desenhar um cartão."""
    return {
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "prioridade": tarefa.prioridade.name.capitalize().replace("Media", "Média"),
        "vencimento": tarefa.data_vencimento.strftime("%d/%m/%Y"),
        "concluida": tarefa.concluida,
        "atrasada": tarefa.esta_atrasada(),
    }
