"""Demonstração da desserialização de uma TarefaSimples.

Execute na raiz do projeto:
    python test_desserializacao.py
"""

from package.tarefa_simples import TarefaSimples


def main():
    dados = {
        "id": 1,
        "titulo": "Estudar Python",
        "descricao": "Revisar programação orientada a objetos",
        "prioridade": "ALTA",
        "data_vencimento": "2025-10-25",  # Data passada intencionalmente
        "concluida": True,
        "tipo": "TarefaSimples",
    }

    print("=== DADOS ORIGINAIS ===")
    print(dados)

    tarefa = TarefaSimples.de_dict(dados)

    print("\n=== OBJETO RECONSTRUÍDO ===")
    print("Classe:", type(tarefa).__name__)
    print("É TarefaSimples?", isinstance(tarefa, TarefaSimples))
    print("Prioridade (enum):", tarefa.prioridade)
    print("Data de vencimento:", tarefa.data_vencimento)
    print("Está atrasada?", tarefa.esta_atrasada())

    recuperado = tarefa.para_dict()
    print("\n=== DICIONÁRIO GERADO APÓS A RECONSTRUÇÃO ===")
    print(recuperado)

    print("\n=== VERIFICAÇÕES ===")
    for chave, valor_esperado in dados.items():
        valor_obtido = recuperado.get(chave)
        ok = valor_obtido == valor_esperado
        print(f"{'OK' if ok else 'FALHOU'} - {chave}: {valor_obtido!r}")
        assert ok, f"Diferença na chave {chave!r}: {valor_obtido!r} != {valor_esperado!r}"

    print("\nSUCESSO: a TarefaSimples foi reconstruída e seus dados foram preservados!")


if __name__ == "__main__":
    main()

