from package.lista import Lista
from package.tarefa import Tarefa

class GerenciadorTarefa:
    
    def __init__(self, lista_tarefas: Lista):
        if not isinstance(lista_tarefas, Lista):
            raise TypeError("O argumento deve ser uma instância de lista")

        self._lista_tarefas = lista_tarefas

    def criar(self, tarefa: Tarefa):
        self._lista_tarefas.adicionar(tarefa)
        
