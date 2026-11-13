from abc import ABC, abstractmethod
from package.prioridade import Prioridade
from datetime import date

class Tarefa(ABC):

    def __init__(self, id: int | None, titulo: str, descricao: str, prioridade: Prioridade, data_vencimento: date):

        if not isinstance(prioridade, Prioridade):
            raise TypeError("Forneça uma prioridade válida!")

        if not isinstance(descricao, str):
            raise TypeError("Descrição deve ser uma string!")

        # Verificação de string para o título
        if isinstance(titulo, str):
            # Verificação para o título não estar vazio
            if not titulo.strip():
                raise ValueError("Título não pode estar vazio!")
        else:
            raise TypeError("O título deve ser uma string!")

        if not isinstance(data_vencimento, date):
            raise TypeError("Forneça a data no formato correto.")

        if id is not None:
            if not isinstance(id, int) or isinstance(id, bool):
                raise TypeError("O ID deve ser um número inteiro!")

            if id <= 0:
                raise ValueError("O ID deve ser maior que zero!")

        self._id = id
        self._prioridade = prioridade
        self._descricao = descricao
        self._concluida = False
        self._titulo = titulo
        self._data_vencimento = data_vencimento

    def editar(self, novo_titulo: str, nova_descricao: str, nova_prioridade: Prioridade, nova_data: date):

        if isinstance(novo_titulo, str):
            if not novo_titulo.strip():
                raise ValueError("O título não pode estar vazio!")
        else:
            raise TypeError("O título deve ser uma string!")

        if not isinstance(nova_descricao, str):
            raise TypeError("A descricação deve ser uma string!")

        if not isinstance(nova_prioridade, Prioridade):
            raise TypeError("Forneça uma prioridade válida!")

        if not isinstance(nova_data, date):
            raise TypeError("A data deve ser uma instância de date!")

        if nova_data != self._data_vencimento and nova_data < date.today():
            raise ValueError("A nova data de vencimento não pode ser anterior à data atual!")

        self._titulo = novo_titulo
        self._descricao = nova_descricao
        self._prioridade = nova_prioridade
        self._data_vencimento = nova_data

    def esta_atrasada(self) -> bool:

        return not self._concluida and date.today() > self._data_vencimento

    def reabrir(self):
        self._concluida = False

    # Dicionário para serialização de objetos

    def para_dict(self):
        tipo = self.__class__.__name__ # Auxilia para encontrar o tipo da tarefa independente de qual seja
        dados_dict = {
            "id": self._id,
            "titulo": self._titulo,
            "descricao": self._descricao,
            "concluida": self._concluida,
            "prioridade": self._prioridade.name, # Serialização especial para JSON convertendo para string
            "data_vencimento": self._data_vencimento.isoformat(), # Serialização especial para JSON convertendo para string
            "tipo": tipo # Serialização especial do tipo de tarefa
        }

        return dados_dict

    def atribuir_id(self, novo_id: int) -> None:
        if self._id is not None:
            raise ValueError("A tarefa já possui um ID.")

        if not isinstance(novo_id, int) or isinstance(novo_id, bool):
            raise TypeError("O ID deve ser um inteiro!")

        if novo_id <= 0:
            raise ValueError("O ID deve ser positivo!")

        self._id = novo_id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def concluida(self) -> bool:
        return self._concluida

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def prioridade(self) -> Prioridade:
        return self._prioridade

    @property
    def data_vencimento(self) -> date:
        return self._data_vencimento

    @abstractmethod
    def concluir(self):
        self._concluida = True
