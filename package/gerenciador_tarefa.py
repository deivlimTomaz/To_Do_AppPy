from package.lista import Lista
from package.tarefa import Tarefa
from package.prioridade import Prioridade
from datetime import date

class GerenciadorTarefa:

    def __init__(self, lista_tarefas: Lista):
        if not isinstance(lista_tarefas, Lista):
            raise TypeError("O argumento deve ser uma instância de lista")

        self._lista_tarefas = lista_tarefas

    def gerar_id(self) -> int:
        tarefas = self._lista_tarefas.tarefas

        if not tarefas:
            return 1

        return max(tarefa.id for tarefa in tarefas) + 1 # Procura o maior ID existente e acrescenta um para uma próxima tarefa criada

    def criar(self, tarefa: Tarefa):
        if not isinstance(tarefa, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        if any(t.id == tarefa.id for t in self._lista_tarefas.tarefas):
            raise ValueError("Já existe uma tarefa com esse ID!")

        if tarefa.data_vencimento < date.today():
            raise ValueError("Erro: a data de vencimento não pode ser anterior à data atual.")

        self._lista_tarefas.adicionar(tarefa)

    def editar(self, tarefa_procurada: Tarefa, novo_titulo: str, nova_descricao: str, nova_prioridade: Prioridade, nova_data: date):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        tarefa = self.buscar_por_id(tarefa_procurada.id)

        tarefa.editar(novo_titulo, nova_descricao, nova_prioridade, nova_data)

        return tarefa

        raise ValueError("Nenhuma tarefa com o ID procurado foi encontrada!")

    # Polimorfismo
    def concluir(self, tarefa_procurada: Tarefa):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        tarefa = self.buscar_por_id(tarefa_procurada.id)

        tarefa.concluir()

        return tarefa

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

    def buscar_por_id(self, id_tarefa: int):
        for tarefa in self._lista_tarefas.tarefas:
            if tarefa.id == id_tarefa:
                return tarefa

        raise ValueError("Tarefa não encontrada")

    @property
    def lista(self):
        return self._lista_tarefas
