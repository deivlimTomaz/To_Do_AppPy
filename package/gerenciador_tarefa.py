from package.lista import Lista
from package.tarefa import Tarefa
from package.prioridade import Prioridade
from datetime import date

class GerenciadorTarefa:

    def __init__(self, lista_tarefas: Lista):
        if not isinstance(lista_tarefas, Lista):
            raise TypeError("O argumento deve ser uma instância de lista")

        self._lista_tarefas = lista_tarefas

    def criar(self, tarefa: Tarefa):
        if not isinstance(tarefa, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        if tarefa.data_vencimento < date.today():
            raise ValueError("Erro: a data de vencimento não pode ser anterior à data atual.")

        self._lista_tarefas.adicionar(tarefa)

    def editar(self, tarefa_procurada: Tarefa, novo_titulo: str, nova_descricao: str, nova_data: date):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        for tarefa_cadastrada in self._lista_tarefas.tarefas:
            if tarefa_cadastrada.id == tarefa_procurada.id:
                tarefa_cadastrada.editar(novo_titulo, nova_descricao, nova_data)
                return tarefa_cadastrada

        raise ValueError("Nenhuma tarefa com o ID procurado foi encontrada!")

    # Polimorfismo
    def concluir(self, tarefa_procurada: Tarefa):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        for tarefa_cadastrada in self._lista_tarefas.tarefas:
            if tarefa_cadastrada.id == tarefa_procurada.id:
                tarefa_cadastrada.concluir()
                return tarefa_cadastrada

        raise ValueError("Nenhuma tarefa com o ID procurado foi encontrada!")

    def excluir(self, tarefa_procurada: Tarefa):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        self._lista_tarefas.remover(tarefa_procurada)

    def filtrar(self, filtrar_prioridade: Prioridade):
        if not isinstance(filtrar_prioridade, Prioridade):
            raise TypeError("A filtragem selecionada não é uma prioridade")

        prioridades_solicitadas = []

        for tarefa_cadastrada in self._lista_tarefas.tarefas:
            if tarefa_cadastrada.prioridade == filtrar_prioridade:
                prioridades_solicitadas.append(tarefa_cadastrada)
        return prioridades_solicitadas
