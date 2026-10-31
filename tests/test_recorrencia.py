from package.recorrencia import Recorrencia
from package.tarefa_recorr import TarefaRecorr
from package.prioridade import Prioridade
from datetime import date, timedelta
import json


def criar_tarefa():
    return TarefaRecorr(
        3,
        "Estudar python",
        "Praticar programação",
        Prioridade.ALTA,
        date.today(),
        Recorrencia("semanal", 2),
    )


def verificar_serializacao(tarefa):
    """Ciclo completo: objeto -> dict -> JSON -> dict -> objeto."""
    original = tarefa.para_dict()
    texto_json = json.dumps(original)
    dados = json.loads(texto_json)

    obj_restaurado = TarefaRecorr.de_dict(dados)
    dict_restaurado = obj_restaurado.para_dict()

    assert isinstance(obj_restaurado, TarefaRecorr), "de_dict não devolveu TarefaRecorr"
    assert dict_restaurado == original, (
        "Dicionários diferem!\n"
        f"Original:   {original}\n"
        f"Restaurado: {dict_restaurado}"
    )
    return obj_restaurado


def teste_pendente():
    tarefa = criar_tarefa()
    restaurada = verificar_serializacao(tarefa)
    assert restaurada.para_dict()["concluida"] is False
    print("OK  - ida e volta (pendente)")


def teste_concluida():
    tarefa = criar_tarefa()
    tarefa.concluir()
    restaurada = verificar_serializacao(tarefa)
    # Valor escrito à mão, independente da comparação de dicionários
    assert restaurada.para_dict()["concluida"] is True
    print("OK  - ida e volta (concluída)")


def teste_intervalo_invalido():
    dados = json.loads(json.dumps(criar_tarefa().para_dict()))
    dados["recorrencia"]["intervalo"] = 0  # chave aninhada
    try:
        TarefaRecorr.de_dict(dados)
    except ValueError:
        print("OK  - intervalo 0 rejeitado com ValueError")
    else:
        raise AssertionError("de_dict aceitou intervalo 0")


def teste_frequencia_invalida():
    dados = json.loads(json.dumps(criar_tarefa().para_dict()))
    dados["recorrencia"]["frequencia"] = "quinzenal"
    try:
        TarefaRecorr.de_dict(dados)
    except ValueError:
        print("OK  - frequência inválida rejeitada com ValueError")
    else:
        raise AssertionError("de_dict aceitou frequência inválida")


def teste_gerar_proxima_pendente():
    tarefa = criar_tarefa()
    try:
        tarefa.gerar_proxima(4)
    except ValueError:
        print("OK  - gerar_proxima recusa tarefa pendente")
    else:
        raise AssertionError("gerar_proxima funcionou em tarefa pendente")


def teste_gerar_proxima_concluida():
    tarefa = criar_tarefa()
    tarefa.concluir()
    proxima = tarefa.gerar_proxima(4)

    dados = proxima.para_dict()
    assert dados["id"] == 4
    assert dados["concluida"] is False
    assert dados["data_vencimento"] == (date.today() + timedelta(weeks=2)).isoformat()
    assert dados["recorrencia"] == tarefa.para_dict()["recorrencia"]

    # A tarefa gerada também precisa sobreviver à ida e volta
    verificar_serializacao(proxima)
    print("OK  - gerar_proxima (data, estado, recorrência e ida e volta)")


def teste_asserts_detectam_diferenca():
    """Sanidade: o assert de comparação realmente falha quando algo muda."""
    original = criar_tarefa().para_dict()
    alterado = dict(original)
    alterado["titulo"] = "Outro título"
    assert alterado != original
    print("OK  - comparação detecta diferença")


if __name__ == "__main__":
    teste_pendente()
    teste_concluida()
    teste_intervalo_invalido()
    teste_frequencia_invalida()
    teste_gerar_proxima_pendente()
    teste_gerar_proxima_concluida()
    teste_asserts_detectam_diferenca()
    print("\nTodos os testes passaram.")
