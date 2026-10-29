from package.tarefa import Tarefa
from package.prioridade import Prioridade
from datetime import date

class TarefaSimples(Tarefa):
    
    def concluir(self):
        super().concluir()
    
    # Desserialização
    @classmethod
    def de_dict(cls, dados: dict):
        
        # Extração de chaves do dicionário de dados
        extract_id = dados["id"]
        extract_titulo = dados["titulo"]
        extract_desc = dados["descricao"]
        
        # Extração especial das prioridades da tarefa
        extract_prioridade = dados["prioridade"]
        extract_prioridade = Prioridade[extract_prioridade]

        # Extreação especial das datas da tarefa
        extract_data = dados["data_vencimento"]
        extract_data = date.fromisoformat(extract_data)

        dados_recuperados = cls(extract_id, extract_titulo, extract_desc, extract_prioridade, extract_data)
        
        extract_estado = dados["concluida"]

        if extract_estado == True:
           dados_recuperados.concluir()

        return dados_recuperados
