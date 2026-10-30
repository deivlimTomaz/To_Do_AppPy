"""Demonstração de TarefaRecorr + Recorrencia, sem unittest ou pytest.

Execute na raiz do projeto: python tests/test_gerar_proxima_recorr.py
Este arquivo pressupõe a versão NOVA de TarefaRecorr que recebe um objeto
Recorrencia e implementa gerar_proxima() como trabalhado nas aulas.
"""

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.tarefa_recorr import TarefaRecorr


def criar_tarefa(identificador, frequencia, intervalo, vencimento):
    return TarefaRecorr(
        identificador,
        f"Tarefa {frequencia}",
        "Demonstração de recorrência",
        Prioridade.ALTA,
        vencimento,
        Recorrencia(frequencia, intervalo),
    )


def demonstrar(nome, frequencia, intervalo, vencimento, novo_id):
    print(f"\n=== {nome} ===")
    tarefa = criar_tarefa(novo_id - 1, frequencia, intervalo, vencimento)
    print("Vencimento original:", tarefa.data_vencimento)
    print("Configuração:", tarefa._recorrencia)

    # É proibido gerar uma ocorrência de uma tarefa não concluída.
    try:
        tarefa.gerar_proxima(novo_id)
    except ValueError as erro:
        print("Bloqueio esperado antes da conclusão:", erro)
    else:
        raise AssertionError("Gerou uma ocorrência sem concluir a original!")

    tarefa.concluir()
    proxima = tarefa.gerar_proxima(novo_id)

    assert isinstance(proxima, TarefaRecorr)
    assert proxima.id == novo_id
    assert proxima.data_vencimento >= date.today()
    assert not proxima._concluida
    assert proxima._recorrencia.frequencia == frequencia
    assert proxima._recorrencia.intervalo == intervalo
    assert proxima._recorrencia is not tarefa._recorrencia

    # Confirma que alterar a recorrência nova não afeta a antiga.
    proxima._recorrencia.intervalo = intervalo + 1
    assert tarefa._recorrencia.intervalo == intervalo
    assert proxima._recorrencia.intervalo == intervalo + 1

    # Confere que a próxima ocorrência pertence à sequência calculada
    # a partir do vencimento original, e não da data de hoje.
    esperada = vencimento
    while esperada < date.today():
        esperada = tarefa._recorrencia.proxima_data(esperada)
    if esperada == vencimento:
        esperada = tarefa._recorrencia.proxima_data(esperada)
    assert proxima.data_vencimento == esperada, (
        f"Data inesperada: {proxima.data_vencimento}, esperada: {esperada}"
    )

    print("Novo vencimento:", proxima.data_vencimento)
    print("Novo ID:", proxima.id)
    print("Nova ocorrência inicia não concluída?", not proxima._concluida)
    print("Recorrências são objetos distintos?", tarefa._recorrencia is not proxima._recorrencia)
    print("Alteração independente do intervalo: OK")
    print("RESULTADO: OK")


print("=== DEMONSTRAÇÃO DE TAREFAS RECORRENTES ===")

hoje = date.today()
demonstrar("1. DIÁRIA", "diaria", 1, hoje, 102)
demonstrar("2. SEMANAL A CADA 2 SEMANAS", "semanal", 2, hoje, 202)
demonstrar("3. MENSAL", "mensal", 1, hoje, 302)
demonstrar("4. ANUAL", "anual", 1, hoje, 402)
demonstrar("5. TAREFA VENCIDA", "semanal", 2, hoje - timedelta(days=45), 502)

print("\n=== 6. CALENDÁRIO: FIM DO MÊS E ANO BISSEXTO ===")
mensal = Recorrencia("mensal", 1)
anual = Recorrencia("anual", 1)
assert mensal.proxima_data(date(2024, 1, 31)) == date(2024, 2, 29)
assert anual.proxima_data(date(2024, 2, 29)) == date(2025, 2, 28)
print("31/01/2024 + 1 mês =", mensal.proxima_data(date(2024, 1, 31)))
print("29/02/2024 + 1 ano =", anual.proxima_data(date(2024, 2, 29)))
print("RESULTADO: OK")

print("\nTODOS OS CENÁRIOS PASSARAM!")

