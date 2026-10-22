import datetime as dt

class Lembrete:

    def __init__(self, data_hora: dt.datetime, mensagem: str):

        # Atributos privados

        self._disparado = False
        self._mensagem = mensagem
        self._data_hora = data_hora

    # Decoradores
    
    @property
    def mensagem(self) -> str:

        return self._mensagem

    @property
    def data_hora(self) -> dt.datetime:

        return self._data_hora

    @property
    def disparado(self) -> bool:

        return self._disparado

    def __str__(self) -> str:

        data_formatada = self.data_hora.strftime("%d/%m/%y às %H:%M")
        status = "[Já disparou]" if self.disparado else "[Agendado]"

        return f"{status} Lembrete: '{self.mensagem}' para o dia {data_formatada}"

