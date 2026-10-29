from package.tarefa import Tarefa
from package.item_checklist import ItemChecklist
from package.prioridade import Prioridade
from datetime import date

class TarefaChecklist(Tarefa):

    def __init__(self, id, titulo, descricao, prioridade, data_vencimento):
        super().__init__(id, titulo, descricao, prioridade, data_vencimento)

        self._itens = []

    def adicionar_item(self, nome: str):

        if not nome.strip():
            raise ValueError("O nome do item não pode estar vazio!")

        if self._concluida:
            raise ValueError("Não é possível adicionar novos itens.")

        novo_item = ItemChecklist(nome)

        self._itens.append(novo_item)

    def marcar_item(self, indice: int):

        if not isinstance(indice, int):
            raise TypeError("O índice é um número!")

        if indice >= len(self._itens) or indice <= -1:
            raise IndexError("Não há essa quantidade de itens na sua tarefa!")

        self._itens[indice].marcar()

    def todos_feitos(self):

        if self._itens == []:
            return False

        if all(item.feito for item in self._itens):
            return True
        else:
            return False

    def concluir(self):

        if self.todos_feitos():
            super().concluir()
        else:
            raise ValueError("A tarefa não pode ser concluída")

    def para_dict(self):
        dados = super().para_dict()
        dados_lista = []

        for item in self._itens:
            dados_lista.append(item.para_dict())

        dados.update({"itens": dados_lista})

        return dados

    @classmethod
    def de_dict(cls, dados: dict):
        # Extração de chaves do dicionário de dados
        extract_id = dados["id"]
        extract_titulo = dados["titulo"]
        extract_desc = dados["descricao"]

        # Extração especial das prioridades da tarefa
        extract_prioridade = dados["prioridade"]
        extract_prioridade = Prioridade[extract_prioridade]

        # Extreação especial das datas da tarefa
        extract_data = dados["data_vencimento"]
        extract_data = date.fromisoformat(extract_data)

        dados_recuperados = cls(extract_id, extract_titulo, extract_desc, extract_prioridade, extract_data)

        extract_lista = dados["itens"]

        for item_recuperado in extract_lista:
            item_recuperado = ItemChecklist.de_dict(item_recuperado)
            dados_recuperados._itens.append(item_recuperado)

        extract_estado = dados["concluida"]

        if extract_estado:
            dados_recuperados.concluir()

        return dados_recuperados
