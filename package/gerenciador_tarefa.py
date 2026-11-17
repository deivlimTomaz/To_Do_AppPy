from package.repositorio import Repositorio
from package.tarefa import Tarefa
from package.tarefa_recorr import TarefaRecorr
from package.prioridade import Prioridade
from package.tarefa_checklist import TarefaChecklist
from datetime import date
from package.repositorio_json import RepositorioJson
from package.fabrica_tarefa import tarefa_de_dict

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

    def reabrir(self, tarefa_procurada: Tarefa):
        if not isinstance(tarefa_procurada, Tarefa):
            raise TypeError("O objeto não é uma tarefa!")

        tarefa = self.buscar_por_id(tarefa_procurada.id)

        tarefa.reabrir()

        self._repositorio.atualizar(tarefa)

        return tarefa

    def adicionar_item(self, id_tarefa: int, texto: str) -> TarefaChecklist:
        tarefa = self.buscar_por_id(id_tarefa)

        if not isinstance(tarefa, TarefaChecklist):
            raise TypeError("A tarefa não é do tipo checklist")

        tarefa.adicionar_item(texto)

        self._repositorio.atualizar(tarefa)

        return tarefa

    def remover_item(self, id_tarefa: int, indice: int) -> TarefaChecklist:
        tarefa = self.buscar_por_id(id_tarefa)

        if not isinstance(tarefa, TarefaChecklist):
            raise TypeError("A tarefa não é do tipo checklist")

        tarefa.remover_item(indice)

        self._repositorio.atualizar(tarefa)

        return tarefa

    def marcar_item(self, id_tarefa: int, indice: int) -> TarefaChecklist:
        tarefa = self.buscar_por_id(id_tarefa)

        if not isinstance(tarefa, TarefaChecklist):
            raise TypeError("A tarefa não é do tipo checklist")

        tarefa.marcar_item(indice)

        self._repositorio.atualizar(tarefa)

        return tarefa

    def desmarcar_item(self, id_tarefa: int, indice: int) -> TarefaChecklist:
        tarefa = self.buscar_por_id(id_tarefa)

        if not isinstance(tarefa, TarefaChecklist):
            raise TypeError("A tarefa não é do tipo checklist")

        tarefa.desmarcar_item(indice)

        self._repositorio.atualizar(tarefa)

        return tarefa

    def gerar_proxima_recorrencia(self, id_tarefa: int) -> TarefaRecorr:
        tarefa = self.buscar_por_id(id_tarefa)

        if not isinstance(tarefa, TarefaRecorr):
            raise TypeError("A tarefa não é do tipo recorrente")

        if not tarefa.concluida:
            raise ValueError("A tarefa não está concluída ainda.")

        proxima = tarefa.gerar_proxima()

        return self.criar(proxima)

    def exportar_json(self, caminho: str) -> None:
        repositorio_json = RepositorioJson(caminho)

        tarefas = self._repositorio.listar()

        dados = [tarefa.para_dict() for tarefa in tarefas]

        repositorio_json.salvar(dados)

    def importar_json(self, caminho: str) -> int:
        repositorio_json = RepositorioJson(caminho)

        dados = repositorio_json.carregar()

        if not isinstance(dados, list):
            raise ValueError("O JSON deve conter uma lista de tarefas.")

        tarefas = []

        for dados_tarefa in dados:
            if not isinstance(dados_tarefa, dict):
                raise ValueError("Cada tarefa deve ser um dicionário.")

            dados_novos = dados_tarefa.copy()
            dados_novos["id"] = None

            tarefa = tarefa_de_dict(dados_novos)
            tarefas.append(tarefa)

        for tarefa in tarefas:
            self.criar(tarefa)

        return len(tarefas)