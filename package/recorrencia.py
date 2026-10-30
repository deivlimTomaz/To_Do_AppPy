from datetime import date

# O relativedelta vem do pacote python-dateutil, que pode ser instalado com pip install python-dateutil
from dateutil.relativedelta import relativedelta

class Recorrencia:

    # Tabela com todas as frequências -> (singular, plural, argumento para relativedelta)
    _FREQUENCIAS = {
            "diaria": ("dia", "dias", "days"),
            "semanal": ("semana", "semanas", "weeks"),
            "mensal": ("mês", "meses", "months"),
            "anual": ("ano", "anos", "years"),
    }

    def __init__(self, frequencia: str, intervalo: int):
        self.frequencia = frequencia
        self.intervalo = intervalo

    # Frequência

    @property
    def frequencia(self) -> str:
        # Retorna a frequência (ex.: 'diaria', 'semanal').
        return self._frequencia

    @frequencia.setter
    def frequencia(self, valor: str):
        # Garante que o valor é um texto
        if not isinstance(valor, str):
            raise TypeError("A frequência deve ser uma string!")

        # Remoção de espaços e padroniza em letras minúsculas
        valor = valor.strip().lower()

        # Só aceita as frequências cadastradas na tabela acima
        if valor not in Recorrencia._FREQUENCIAS:
            raise ValueError(f"Frequência inválida! Escolha entre: {list(Recorrencia._FREQUENCIAS)}")

        self._frequencia = valor

    # Intervalo

    @property
    def intervalo(self) -> int:
        # Retorna de quantas em quantas unidades a tarefa se repete
        return self._intervalo

    @intervalo.setter
    def intervalo(self, valor: int):
        # Garante que o valor é inteiro
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("O intervalo precisa ser um inteiro!")

        # Intervalo não pode ser negativo e nem zero
        if valor <= 0:
            raise ValueError("Intervalo inválido!")

        self._intervalo = valor


    # Comportamento

    def __str__(self) -> str:
        # Devolve a recorrência em texto legível
        # Pega apenas singular e plural da tabela (itens relacionados ao relativedelta são ignorados)
        singular, plural, _ = Recorrencia._FREQUENCIAS[self._frequencia]


        # Intervalo 1 usa o singular ("A cada semana")
        # Qualquer outro usa o número e o plural ("A cada 3 semanas")
        if self._intervalo == 1:
            return f"A cada {singular}"
        return f"A cada {self._intervalo} {plural}"

    def proxima_data(self, data_base: date = None) -> date:
        # Calcula a próxima data de recorrência a partir de uma data base
        # Se nenhuma data for passada, usa a data de hoje
        if data_base is None:
            data_base = date.today()

        if not isinstance(data_base, date):
            raise TypeError("Data não está no formato correto!")

        # Descobre o nome do argumento do relativedelta ("days", "weeks", ...)
        _, _, argumento_tempo = Recorrencia._FREQUENCIAS[self._frequencia]

        # Monta algo como relativedelta(weeks=2) e soma à data base
        # O relativedelta ajusta sozinho meses de tamanhos diferentes
        # (ex.: 31/01 + 1 mês = 28/02)
        return data_base + relativedelta(**{argumento_tempo: self._intervalo})
