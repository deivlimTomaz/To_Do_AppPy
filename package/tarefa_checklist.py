from package.tarefa import Tarefa
from package.item_checklist import ItemChecklist

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
