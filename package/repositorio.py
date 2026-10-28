from abc import ABC, abstractmethod

class Repositorio(ABC):

    @abstractmethod
    def salvar(self, dados):
        pass

    @abstractmethod
    def carregar(self):
        pass
