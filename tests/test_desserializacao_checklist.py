
from datetime import date
from package.tarefa_checklist import TarefaChecklist
from package.prioridade import Prioridade
from package.item_checklist import ItemChecklist


def demonstrar_desserializacao(nome_cenario, tarefa_original):
    print("\n" + "=" * 65)
    print(nome_cenario)
    print("=" * 65)

    # 1. Serialização
    dados_originais = tarefa_original.para_dict()

    print("\n=== DADOS ORIGINAIS ===")
    print(dados_originais)

    # 2. Desserialização
    tarefa_recuperada = TarefaChecklist.de_dict(dados_originais)

    print("\n=== OBJETO RECONSTRUÍDO ===")
    print("Classe:", type(tarefa_recuperada).__name__)
    print("É TarefaChecklist?", isinstance(tarefa_recuperada, TarefaChecklist))
    print("Prioridade:", tarefa_recuperada.prioridade)
    print("Data de vencimento:", tarefa_recuperada.data_vencimento)
    print("Todos os itens feitos?", tarefa_recuperada.todos_feitos())

    print("\n=== ITENS RECONSTRUÍDOS ===")
    for indice, item in enumerate(tarefa_recuperada._itens):
        print(f"Item {indice + 1}: {item}")
        print("É ItemChecklist?", isinstance(item, ItemChecklist))

    # 3. Nova serialização
    dados_recuperados = tarefa_recuperada.para_dict()

    print("\n=== DICIONÁRIO APÓS RECONSTRUÇÃO ===")
    print(dados_recuperados)

    # 4. Verificações
    print("\n=== VERIFICAÇÕES ===")

    for chave, valor_original in dados_originais.items():
        valor_recuperado = dados_recuperados.get(chave)

        if valor_original == valor_recuperado:
            print(f"OK - {chave}: {valor_recuperado!r}")
        else:
            print(f"ERRO - {chave}")
            print(f"  Original: {valor_original!r}")
            print(f"  Recuperado: {valor_recuperado!r}")

    assert isinstance(tarefa_recuperada, TarefaChecklist)
    assert all(
        isinstance(item, ItemChecklist)
        for item in tarefa_recuperada._itens
    )
    assert dados_originais == dados_recuperados, (
        "Os dados não foram preservados!"
    )

    print("\nSUCESSO: tarefa reconstruída e dados preservados!")


# ==========================================================
# CENÁRIO 1: CHECKLIST PARCIALMENTE CONCLUÍDA
# ==========================================================

tarefa1 = TarefaChecklist(
    1,
    "Estudar Python",
    "Revisar conceitos de POO",
    Prioridade.ALTA,
    date(2026, 12, 10)
)

tarefa1.adicionar_item("Estudar herança")
tarefa1.adicionar_item("Estudar polimorfismo")
tarefa1.adicionar_item("Estudar encapsulamento")

tarefa1.marcar_item(0)
tarefa1.marcar_item(2)

demonstrar_desserializacao(
    "CENÁRIO 1 - CHECKLIST PARCIALMENTE CONCLUÍDA",
    tarefa1
)


# ==========================================================
# CENÁRIO 2: CHECKLIST TOTALMENTE CONCLUÍDA
# ==========================================================

tarefa2 = TarefaChecklist(
    2,
    "Finalizar projeto",
    "Concluir atividades do gerenciador",
    Prioridade.ALTA,
    date(2026, 12, 15)
)

tarefa2.adicionar_item("Implementar classes")
tarefa2.adicionar_item("Implementar serialização")
tarefa2.adicionar_item("Implementar desserialização")

tarefa2.marcar_item(0)
tarefa2.marcar_item(1)
tarefa2.marcar_item(2)

tarefa2.concluir()

demonstrar_desserializacao(
    "CENÁRIO 2 - CHECKLIST TOTALMENTE CONCLUÍDA",
    tarefa2
)


# ==========================================================
# CENÁRIO 3: CHECKLIST SEM ITENS
# ==========================================================

tarefa3 = TarefaChecklist(
    3,
    "Planejar estudos",
    "Organizar conteúdos futuros",
    Prioridade.MEDIA,
    date(2026, 12, 20)
)

demonstrar_desserializacao(
    "CENÁRIO 3 - CHECKLIST SEM ITENS",
    tarefa3
)


# ==========================================================
# CENÁRIO 4: CHECKLIST COM DATA VENCIDA
# ==========================================================

tarefa4 = TarefaChecklist(
    4,
    "Revisar conteúdo antigo",
    "Atividade com vencimento no passado",
    Prioridade.BAIXA,
    date(2025, 10, 25)
)

tarefa4.adicionar_item("Revisar classes")
tarefa4.adicionar_item("Revisar objetos")
tarefa4.marcar_item(0)

demonstrar_desserializacao(
    "CENÁRIO 4 - CHECKLIST VENCIDA",
    tarefa4
)


print("\n" + "=" * 65)
print("TODOS OS CENÁRIOS FORAM EXECUTADOS COM SUCESSO!")
print("=" * 65)

