"""Conversão e criação de tarefas simples a partir de dados de formulário."""
from datetime import date, datetime

from package.gerenciador_tarefa import GerenciadorTarefa
from package.prioridade import Prioridade
from package.tarefa_simples import TarefaSimples


PRIORIDADES = {"Baixa": Prioridade.BAIXA, "Média": Prioridade.MEDIA, "Alta": Prioridade.ALTA}


def criar_tarefa_simples(gerenciador: GerenciadorTarefa, titulo: str,
                         descricao: str, prioridade: str, vencimento: str) -> TarefaSimples:
    """Valida entrada de formulário (DD/MM/AAAA) e persiste via gerenciador."""
    if not titulo.strip():
        raise ValueError("Informe o título da tarefa.")

    try:
        prioridade_enum = PRIORIDADES[prioridade]
    except KeyError as erro:
        raise ValueError("Selecione uma prioridade válida.") from erro

    try:
        data_vencimento = datetime.strptime(vencimento.strip(), "%d/%m/%Y").date()
    except ValueError as erro:
        raise ValueError("Informe uma data válida no formato DD/MM/AAAA.") from erro

    if data_vencimento < date.today():
        raise ValueError("A data de vencimento não pode estar no passado.")

    tarefa = TarefaSimples(None, titulo.strip(), descricao.strip(),
                          prioridade_enum, data_vencimento)
    return gerenciador.criar(tarefa)
