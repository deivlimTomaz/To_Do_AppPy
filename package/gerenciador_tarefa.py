from package.repositorio import Repositorio
from package.tarefa import Tarefa
from package.prioridade import Prioridade
from datetime import date

class GerenciadorTarefa:

    def __init__(self, repositorio: Repositorio):
        if not isinstance(repositorio, Repositorio):
            raise TypeError("O argumento deve ser uma instância de Repositorio")

        self._repositorio = repositorio

    def criar(self, tarefa: Tarefa) -> Tarefa:
        if not isinstance(tarefa, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        if tarefa.id is not None:
            raise ValueError("A tarefa já possui um ID.")

        if tarefa.data_vencimento < date.today():
            raise ValueError("Erro: a data de vencimento não pode ser anterior à data atual.")

        return self._repositorio.adicionar(tarefa)

    def editar(self, tarefa_procurada: Tarefa, novo_titulo: str, nova_descricao: str, nova_prioridade: Prioridade, nova_data: date):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        tarefa = self.buscar_por_id(tarefa_procurada.id)

        tarefa.editar(novo_titulo, nova_descricao, nova_prioridade, nova_data)

        self._repositorio.atualizar(tarefa)

        return tarefa

    # Polimorfismo
    def concluir(self, tarefa_procurada: Tarefa):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        tarefa = self.buscar_por_id(tarefa_procurada.id)

        tarefa.concluir()

        self._repositorio.atualizar(tarefa)

        return tarefa

    def excluir(self, tarefa_procurada: Tarefa):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        if tarefa_procurada.id is None:
            raise ValueError("Não é possível excluir uma tarefa sem ID.")

        self._repositorio.remover(tarefa_procurada.id)

    def filtrar(self, filtrar_prioridade: Prioridade):
        if not isinstance(filtrar_prioridade, Prioridade):
            raise TypeError("A filtragem selecionada não é uma prioridade")

        prioridades_solicitadas = []

        for tarefa_cadastrada in self._repositorio.listar():
            if tarefa_cadastrada.prioridade == filtrar_prioridade:
                prioridades_solicitadas.append(tarefa_cadastrada)
        return prioridades_solicitadas

    def buscar_por_id(self, id_tarefa: int) -> Tarefa:
        tarefa = self._repositorio.buscar_por_id(id_tarefa)

        if tarefa is None:
            raise ValueError("Tarefa não encontrada")

        return tarefa

    def listar(self) -> list[Tarefa]:
        return self._repositorio.listar()
