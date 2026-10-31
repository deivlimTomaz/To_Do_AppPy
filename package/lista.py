from package.tarefa import Tarefa
from package.categoria import Categoria
from package.fabrica_tarefa import tarefa_de_dict

class Lista:

    def __init__(self, nome: str, categoria: Categoria):

        if not isinstance(nome, str):
            raise TypeError("O nome deve ser uma string")

        if not isinstance(categoria, Categoria):
            raise TypeError("Erro: Categoria inválida")

        if not nome.strip():
            raise ValueError("Nome da lista não pode estar em branco!")

        self._nome = nome
        self._categoria = categoria
        self._tarefas = []

    def adicionar(self, tarefa: Tarefa):

        if not isinstance(tarefa, Tarefa):
            raise TypeError("O objeto deve ser uma tarefa")

        if any(i.id == tarefa.id for i in self._tarefas):
            raise ValueError("A tarefa já existe na lista.")

        self._tarefas.append(tarefa)

    def remover(self, tarefa: Tarefa):
        if not isinstance(tarefa, Tarefa):
            raise TypeError("O objeto deve ser uma tarefa")

        for indice, t in enumerate(self._tarefas):
            if t.id == tarefa.id:
                return self._tarefas.pop(indice)

        raise ValueError("Tarefa com ID especificado não foi encontrada")

    @property
    def tarefas(self):
        return self._tarefas.copy()

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def nome(self) -> str:
        return self._nome

    def para_dict(self):
        return {
            "nome": self._nome,
            "categoria": self._categoria.para_dict(),
            "tarefas": [tarefa.para_dict() for tarefa in self._tarefas]
        }

    @classmethod
    def de_dict(cls, dados):
        categoria = Categoria.de_dict(dados["categoria"])

        lista = cls(
            dados["nome"],
            categoria
        )

        for tarefa in dados["tarefas"]:
            lista.adicionar(tarefa_de_dict(tarefa))

        return lista
