from abc import ABC, abstractmethod
from package.prioridade import Prioridade
from datetime import date

class Tarefa(ABC):

    def __init__(self, id: int, titulo: str, descricao: str, prioridade: Prioridade, data_vencimento: date):
        self._id = id
        self._prioridade = prioridade
        self._descricao = descricao
        self._concluida = False

        if not titulo.strip():
            raise ValueError("Título não pode estar vazio!")
    
        self._titulo = titulo

        if data_vencimento < date.today():
            raise ValueError("A data de vencimento não pode ser uma data passada!")

        self._data_vencimento = data_vencimento

    def editar(self, novo_titulo: str, nova_descricao: str, nova_data: date):
        
        if not novo_titulo.strip():
            raise ValueError("Título não pode estar vazio!")
        
        if nova_data < date.today():
            raise ValueError("A data de vencimento não pode ser uma data passada!")

        self._titulo = novo_titulo
        self._descricao = nova_descricao
        self._data_vencimento = nova_data

    def esta_atrasada(self) -> bool:
    
        return not self._concluida and date.today() > self._data_vencimento

    @abstractmethod
    def proximo_estado(self):
        pass

    @abstractmethod
    def concluir(self):
        self._concluida = True
