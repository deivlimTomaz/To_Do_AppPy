from abc import ABC, abstractmethod
from package.prioridade import Prioridade
from datetime import date

class Tarefa(ABC):

    def __init__(self, id: int, titulo: str, descricao: str, prioridade: Prioridade, data_vencimento: date):
        self._id = id
        self._prioridade = prioridade
        self._descricao = descricao
        self._concluida = False

        # Verificação de string para o título
        if isinstance(titulo, str):
            # Verificação para o título não estar vazio
            if not titulo.strip():
                raise ValueError("Título não pode estar vazio!")
        else:
            raise TypeError("O título deve ser uma string!")

        self._titulo = titulo

        if not isinstance(data_vencimento, date):
            raise TypeError("Forneça a data no formato correto.")

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

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def concluir(self):
        self._concluida = True

    @property
    def prioridade(self) -> Prioridade:
        return self._prioridade

    @property
    def data_vencimento(self) -> date:
        return self._data_vencimento
