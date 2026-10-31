from package.tarefa_simples import TarefaSimples
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr

_TIPOS = {
    "TarefaSimples": TarefaSimples,
    "TarefaRecorr": TarefaRecorr,
    "TarefaChecklist": TarefaChecklist
}

def tarefa_de_dict(dados: dict):
    tipo_nome = dados.get("tipo")

    if not tipo_nome:
        raise ValueError("Os dados fornecidos não contêm a chave obrigatória 'tipo'")

    if tipo_nome not in _TIPOS:
        tipos_validos = ", ".join(_TIPOS.keys())
        raise ValueError(
            f"Tipo de tarefa desconhecido: '{tipo_nome}'."
            f"Os tipos válidos são: [{tipos_validos}]."
        )

    classe_tarefa = _TIPOS[tipo_nome]
    return classe_tarefa.de_dict(dados)
