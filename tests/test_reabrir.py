"""Testes de Tarefa.reabrir() (Fase 1, tópico 5).

Execute a partir da raiz do projeto:
    python -m tests.test_reabrir
"""

import json
import sys
from datetime import date, timedelta

from package.fabrica_tarefa import tarefa_de_dict
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.tarefa_simples import TarefaSimples

contagem = {"ok": 0, "falha": 0}


def separar(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def verificar(condicao, descricao):
    contagem["ok" if condicao else "falha"] += 1
    print(f"{'OK' if condicao else 'FALHA'}: {descricao}")


def esperar_erro(tipo_erro, descricao, acao):
    try:
        acao()
    except tipo_erro as erro:
        verificar(True, f"{descricao} -> {tipo_erro.__name__}: {erro}")
    except Exception as erro:
        verificar(False, f"{descricao} -> esperado {tipo_erro.__name__}, "
                         f"veio {type(erro).__name__}: {erro}")
    else:
        verificar(False, f"{descricao} -> nenhum erro foi lançado")


def futuro(dias=5):
    return date.today() + timedelta(days=dias)


def simples(vencimento=None):
    return TarefaSimples(1, "Estudar", "Revisar o capítulo", Prioridade.ALTA,
                         vencimento or futuro())


def checklist(qtd_itens=2):
    tarefa = TarefaChecklist(2, "Preparar", "Slides", Prioridade.MEDIA, futuro())
    for numero in range(1, qtd_itens + 1):
        tarefa.adicionar_item(f"Item {numero}")
    return tarefa


def checklist_concluida():
    tarefa = checklist()
    tarefa.marcar_item(0)
    tarefa.marcar_item(1)
    tarefa.concluir()
    return tarefa


def recorrente():
    return TarefaRecorr(3, "Beber água", "Todo dia", Prioridade.BAIXA, futuro(1),
                        Recorrencia("diaria", 1))


# ---------------------------------------------------------------
separar("TESTE 1 - CONCLUÍDA -> PENDENTE (TarefaSimples)")
tarefa = simples()
verificar(not tarefa.concluida, "tarefa nova começa pendente")
tarefa.concluir()
verificar(tarefa.concluida, "concluir() marca como concluída")
tarefa.reabrir()
verificar(not tarefa.concluida, "reabrir() volta para pendente")
tarefa.concluir()
verificar(tarefa.concluida, "dá para concluir de novo depois de reabrir")

# ---------------------------------------------------------------
separar("TESTE 2 - reabrir NÃO ALTERA OS DEMAIS DADOS")
tarefa = simples()
antes = (tarefa.id, tarefa.titulo, tarefa.descricao, tarefa.prioridade, tarefa.data_vencimento)
tarefa.concluir()
tarefa.reabrir()
depois = (tarefa.id, tarefa.titulo, tarefa.descricao, tarefa.prioridade, tarefa.data_vencimento)
verificar(antes == depois, "id, título, descrição, prioridade e vencimento intactos")

# ---------------------------------------------------------------
separar("TESTE 3 - reabrir EM TAREFA QUE JÁ ESTÁ PENDENTE (decisão atual: não faz nada)")
tarefa = simples()
try:
    tarefa.reabrir()
    verificar(not tarefa.concluida, "sem erro e continua pendente")
    tarefa.reabrir()
    tarefa.reabrir()
    verificar(not tarefa.concluida, "chamar várias vezes seguidas é inofensivo")
except Exception as erro:
    verificar(False, f"lançou {type(erro).__name__}: {erro} "
                     "(se você decidiu exigir ValueError, ajuste este teste)")

# ---------------------------------------------------------------
separar("TESTE 4 - INTERAÇÃO COM esta_atrasada")
tarefa = simples(vencimento=date.today() - timedelta(days=3))
verificar(tarefa.esta_atrasada(), "vencida e pendente: atrasada")
tarefa.concluir()
verificar(not tarefa.esta_atrasada(), "vencida e concluída: não está atrasada")
tarefa.reabrir()
verificar(tarefa.esta_atrasada(), "reaberta e ainda vencida: volta a ficar atrasada")
em_dia = simples()
em_dia.concluir()
em_dia.reabrir()
verificar(not em_dia.esta_atrasada(), "reaberta mas com prazo futuro: não está atrasada")

# ---------------------------------------------------------------
separar("TESTE 5 - CHECKLIST: OPERAÇÕES DE ITEM VOLTAM A SER PERMITIDAS")
tarefa = checklist_concluida()
esperar_erro(ValueError, "concluída: adicionar item", lambda: tarefa.adicionar_item("Novo"))
esperar_erro(ValueError, "concluída: desmarcar item", lambda: tarefa.desmarcar_item(0))
esperar_erro(ValueError, "concluída: remover item", lambda: tarefa.remover_item(0))
tarefa.reabrir()
verificar(not tarefa.concluida, "checklist reaberto fica pendente")
try:
    tarefa.adicionar_item("Item 3")
    tarefa.desmarcar_item(0)
    tarefa.marcar_item(0)
    tarefa.remover_item(2)
    verificar(True, "reaberta: adicionar, desmarcar, marcar e remover item funcionam")
except Exception as erro:
    verificar(False, f"operação de item falhou depois de reabrir: {type(erro).__name__}: {erro}")

# ---------------------------------------------------------------
separar("TESTE 6 - CHECKLIST: O QUE ACONTECE COM OS ITENS (decisão atual: continuam marcados)")
tarefa = checklist_concluida()
tarefa.reabrir()
verificar(tarefa.progresso() == (2, 2), "itens continuam marcados: progresso (2, 2)")
verificar(tarefa.todos_feitos(), "todos_feitos continua True")
tarefa.concluir()
verificar(tarefa.concluida, "dá para concluir de novo sem mexer nos itens")
tarefa.reabrir()
esperar_erro(ValueError, "reaberta com item pendente: concluir() recusa",
             lambda: (tarefa.desmarcar_item(1), tarefa.concluir()))
verificar(not tarefa.concluida, "e continua pendente")

# ---------------------------------------------------------------
separar("TESTE 7 - RECORRENTE")
tarefa = recorrente()
esperar_erro(ValueError, "pendente: gerar_proxima recusa", lambda: tarefa.gerar_proxima(10))
tarefa.concluir()
proxima = tarefa.gerar_proxima(10)
verificar(isinstance(proxima, TarefaRecorr) and not proxima.concluida,
          "concluída: gerar_proxima devolve nova ocorrência pendente")
tarefa.reabrir()
verificar(not tarefa.concluida, "ocorrência original reaberta fica pendente")
esperar_erro(ValueError, "reaberta: gerar_proxima volta a recusar", lambda: tarefa.gerar_proxima(11))
verificar(tarefa.data_vencimento == futuro(1), "reabrir não muda a data da ocorrência")
verificar(not proxima.concluida, "reabrir a original não mexe na próxima já gerada")

# ---------------------------------------------------------------
separar("TESTE 8 - SERIALIZAÇÃO DEPOIS DE reabrir")
for nome, criar in (("simples", simples), ("checklist", checklist_concluida), ("recorrente", recorrente)):
    tarefa = criar()
    if nome == "checklist":
        pass  # já vem concluída
    else:
        tarefa.concluir()
    dados = tarefa.para_dict()
    verificar(dados["concluida"] is True, f"{nome}: para_dict mostra concluida=True")
    tarefa.reabrir()
    dados = tarefa.para_dict()
    verificar(dados["concluida"] is False, f"{nome}: para_dict mostra concluida=False depois de reabrir")
    try:
        texto = json.dumps(dados)
        copia = tarefa_de_dict(json.loads(texto))
        verificar(not copia.concluida and type(copia) is type(tarefa),
                  f"{nome}: ida e volta por JSON volta pendente e do mesmo tipo")
    except Exception as erro:
        verificar(False, f"{nome}: ida e volta por JSON falhou: {type(erro).__name__}: {erro}")

# ---------------------------------------------------------------
separar("RESUMO")
print(f"{contagem['ok']} OK | {contagem['falha']} FALHA")
sys.exit(1 if contagem["falha"] else 0)
