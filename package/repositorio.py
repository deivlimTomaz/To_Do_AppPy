from abc import ABC, abstractmethod
from package.tarefa import Tarefa

class Repositorio(ABC):

    @abstractmethod
    def adicionar(self, tarefa: Tarefa) -> Tarefa:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Tarefa | None:
        pass

    @abstractmethod
    def listar(self) -> list[Tarefa]:
        pass

    @abstractmethod
    def atualizar(self, tarefa: Tarefa) -> None:
        pass

    @abstractmethod
    def remover(self, id: int) -> None:
        pass

