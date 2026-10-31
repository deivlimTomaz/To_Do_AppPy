"""
Teste de ida e volta da serialização de Lista.

Coloque este arquivo na pasta tests/ e rode a partir da raiz do projeto:
    python tests/test_lista_serializacao.py
"""
import json
import os
import sys
import tempfile
from datetime import date, timedelta

# Permite importar "package" mesmo rodando de dentro de tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from package.categoria import Categoria
from package.lista import Lista
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.repositorio_json import RepositorioJson
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.tarefa_simples import TarefaSimples
from package.fabrica_tarefa import tarefa_de_dict

amanha = date.today() + timedelta(days=1)
semana_que_vem = date.today() + timedelta(days=7)


def montar_lista() -> Lista:
    lista = Lista("Faculdade", Categoria("azul", "estudo"))

    # 1. Simples, pendente
    simples = TarefaSimples(1, "Estudar POO", "Capítulo 3", Prioridade.ALTA, amanha)

    # 2. Simples, já concluída
    simples_ok = TarefaSimples(2, "Entregar lista", "IAL bloco 4", Prioridade.BAIXA, amanha)
    simples_ok.concluir()

    # 3. Checklist parcialmente feita (não concluída)
    check_parcial = TarefaChecklist(3, "Compras", "Mercado", Prioridade.MEDIA, semana_que_vem)
    check_parcial.adicionar_item("Arroz")
    check_parcial.adicionar_item("Feijão")
    check_parcial.marcar_item(0)

    # 4. Checklist toda feita e concluída
    #    (caso sensível: itens precisam ser recarregados ANTES de concluir())
    check_ok = TarefaChecklist(4, "Mala de viagem", "Fim de semana", Prioridade.MEDIA, semana_que_vem)
    check_ok.adicionar_item("Roupas")
    check_ok.adicionar_item("Carregador")
    check_ok.marcar_item(0)
    check_ok.marcar_item(1)
    check_ok.concluir()

    # 5. Recorrente pendente
    recorr = TarefaRecorr(5, "Academia", "Treino A", Prioridade.ALTA, amanha, Recorrencia("semanal", 2))

    # 6. Recorrente concluída
    recorr_ok = TarefaRecorr(6, "Pagar internet", "Todo mês", Prioridade.BAIXA, amanha, Recorrencia("mensal", 1))
    recorr_ok.concluir()

    for tarefa in (simples, simples_ok, check_parcial, check_ok, recorr, recorr_ok):
        lista.adicionar(tarefa)

    return lista


def comparar(original: Lista, recuperada: Lista, rotulo: str):
    assert recuperada.nome == original.nome, f"[{rotulo}] nome da lista diferente"
    assert recuperada.categoria.para_dict() == original.categoria.para_dict(), \
        f"[{rotulo}] categoria diferente"

    originais = original.tarefas
    recuperadas = recuperada.tarefas
    assert len(recuperadas) == len(originais), \
        f"[{rotulo}] quantidade de tarefas: {len(recuperadas)} != {len(originais)}"

    for o, r in zip(originais, recuperadas):
        assert type(r) is type(o), \
            f"[{rotulo}] tarefa {o.id}: tipo {type(r).__name__} != {type(o).__name__}"
        assert r.para_dict() == o.para_dict(), \
            f"[{rotulo}] tarefa {o.id}: dados diferentes\n  original:  {o.para_dict()}\n  recuperada: {r.para_dict()}"
        print(f"  OK  id={o.id}  {type(o).__name__}")


def teste_ida_e_volta_em_memoria():
    print("\n[1] Ida e volta em memória (json.dumps / json.loads)")
    original = montar_lista()
    texto_json = json.dumps(original.para_dict(), ensure_ascii=False)
    recuperada = Lista.de_dict(json.loads(texto_json))
    comparar(original, recuperada, "memória")


def teste_ida_e_volta_em_arquivo():
    print("\n[2] Ida e volta com RepositorioJson (arquivo)")
    original = montar_lista()

    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "lista.json")
        repo = RepositorioJson(caminho)
        repo.salvar(original.para_dict())
        recuperada = Lista.de_dict(repo.carregar())

    comparar(original, recuperada, "arquivo")


def teste_tipo_desconhecido():
    print("\n[3] Fábrica com tipo desconhecido")
    try:
        tarefa_de_dict({"tipo": "TarefaInexistente"})
    except ValueError as erro:
        print(f"  OK  ValueError: {erro}")
    else:
        raise AssertionError("Deveria ter levantado ValueError para tipo desconhecido")


def teste_tipo_ausente():
    print("\n[4] Fábrica com chave 'tipo' ausente")
    try:
        tarefa_de_dict({"id": 1})
    except ValueError as erro:
        print(f"  OK  ValueError: {erro}")
    else:
        raise AssertionError("Deveria ter levantado ValueError para 'tipo' ausente")


if __name__ == "__main__":
    teste_ida_e_volta_em_memoria()
    teste_ida_e_volta_em_arquivo()
    teste_tipo_desconhecido()
    teste_tipo_ausente()
    print("\nTodos os testes passaram.")
