from package.tarefa import Tarefa
from package.recorrencia import Recorrencia
from package.prioridade import Prioridade
from datetime import date, timedelta

class TarefaRecorr(Tarefa):
    def __init__(self, id, titulo, descricao, prioridade, data_vencimento, recorr: Recorrencia):
        super().__init__(id, titulo, descricao, prioridade, data_vencimento)

        if not isinstance(recorr, Recorrencia):
            raise TypeError("O objeto não é uma instância de recorrência")

        self._recorrencia = recorr

    def gerar_proxima(self, novo_id):
        frequencia = self._recorrencia.frequencia
        intervalo = self._recorrencia.intervalo

        # Só pode ser calculada uma nova data se a tarefa na data anterior for concluída
        if self._concluida == False:
            raise ValueError("A tarefa precisa ser concluída primeiro")

        # Calcular a próxima data de vencimento da tarefa recorrente
        calc_prox_data = self._recorrencia.proxima_data(self._data_vencimento)

        # Avança a partir da última ocorrência calculada e passa a calcular a data
        while calc_prox_data < date.today():
            calc_prox_data = self._recorrencia.proxima_data(calc_prox_data)

        nova_recorrencia = Recorrencia(frequencia, intervalo)

        proxima_tarefa = TarefaRecorr(novo_id, self._titulo, self._descricao, self._prioridade, calc_prox_data, nova_recorrencia)

        return proxima_tarefa

    def concluir(self):
        super().concluir()

    def para_dict(self):
        # Armazena o dicionário herdado
        dados = super().para_dict()

        dados.update({"recorrencia": self._recorrencia.para_dict()})

        return dados

    @classmethod
    def de_dict(cls, dados: dict):
        # Lendo cada dado do dicionário
        extract_id = dados["id"]
        extract_titulo = dados["titulo"]
        extract_desc = dados["descricao"]

        # Extração especial das prioridades
        extract_prioridade = dados["prioridade"]
        extract_prioridade = Prioridade[extract_prioridade]

        # Extreação especial das datas da tarefa
        extract_data = dados["data_vencimento"]
        extract_data = date.fromisoformat(extract_data)

        extract_recorr = Recorrencia.de_dict(dados["recorrencia"])

        dados_recuperados = cls(extract_id, extract_titulo, extract_desc, extract_prioridade, extract_data, extract_recorr)

        extract_estado = dados["concluida"]

        if extract_estado:
            dados_recuperados.concluir()

        return dados_recuperados
