from datetime import datetime
from dateutil.relativedelta import relativedelta

class Recorrencia:
    
    VALORES_ACEITOS = ["diaria", "semanal", "mensal", "anual"]

    def __init__(self, frequencia: str, intervalo: int):

        self.frequencia = frequencia
        self.intervalo = intervalo

    @property
    def frequencia(self) -> str:
        return self._frequencia

    @property
    def intervalo(self) -> int:
        return self._intervalo

    @frequencia.setter
    def frequencia(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError("A frequência deve ser uma string!")

        if valor.lower() not in Recorrencia.valores_aceitos:
            raise ValueError(f"Frequência inválida! Escolha entre: {Recorrencia.valores_aceitos}")

        self._frequencia = valor.lower()
        
    @intervalo.setter
    def intervalo(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("O intervalo precisa ser um inteiro!")

        if valor <= 0:
            raise ValueError("Intervalo inválido!")

        self._intervalo = valor


    def __str__(self) -> str:

        mapeamento = {
                "diaria": ("dia", "dias")
                "semanal": ("semana", "semanas")
                "mensal": ("mês", "meses")
                "anual": ("ano", "anos")
        }

        singular, plural = mapeamento[self._frequencia]

        if self._intervalo == 1:
            return f"A cada {singular}"

        else:
            return f"A cada {self._intervalo} {plural}"

    def proxima_data(self, data_base: datetime = None) -> datetime:
        if data_base is None:
            data_base = datetime.now()

        mapeamento_delta = {
                "diaria": "days",
                "semanal": "weeks",
                "mensal": "months",
                "anual": "years"
        }

        argumento_tempo = mapeamento_delta[self._frequencia]

        argumentos {argumento_tempo: self._intervalo}

        return data_base + relativedelta(**argumentos)
        
