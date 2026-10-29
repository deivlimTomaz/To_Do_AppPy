from package.tarefa import Tarefa
from datetime import date, timedelta

class TarefaRecorr(Tarefa):
    def __init__(self, id, titulo, descricao, prioridade, data_vencimento, frequencia: str):
        super().__init__(id, titulo, descricao, prioridade, data_vencimento)

        if not isinstance(frequencia, str):
            raise TypeError("Frequência deve ser uma string")

        if not frequencia == "diaria" and not frequencia == "semanal":
            raise ValueError("Frequência deve ser diária ou semanal")
            
        
        self._frequencia = frequencia

    
    def gerar_proxima(self, novo_id):
        if self._frequencia == "diaria":
            intervalo = timedelta(days=1)
        elif self._frequencia == "semanal":
            intervalo = timedelta(days=7)
        
        if self._concluida == False:
            raise ValueError("A tarefa precisa ser concluída primeiro")

        nova_data_venc = self._data_vencimento + intervalo
        
        while nova_data_venc < date.today():
            nova_data_venc += intervalo

        proxima_tarefa = TarefaRecorr(novo_id, self._titulo, self._descricao, self._prioridade, nova_data_venc, self._frequencia)
        

        return proxima_tarefa

    def concluir(self):
        super().concluir()

    def para_dict(self):
        super().para_dict()

