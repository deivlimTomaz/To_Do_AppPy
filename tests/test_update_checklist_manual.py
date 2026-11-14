from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.prioridade import Prioridade
from package.tarefa_checklist import TarefaChecklist
from package.repositorio_sqlite import RepositorioSQLite


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_update_checklist.db")

    conexao = conectar(caminho_db)

    try:
        sql = Path("schema.sql").read_text(encoding="utf-8")
        conexao.executescript(sql)
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    tarefa = TarefaChecklist(
        None,
        "Estudar Python",
        "Revisar conceitos",
        Prioridade.ALTA,
        date(2026, 11, 20)
    )

    tarefa.adicionar_item("Classes")
    tarefa.adicionar_item("Herança")
    tarefa.adicionar_item("Polimorfismo")

    repositorio.adicionar(tarefa)

    # Marcar um item e persistir
    tarefa.marcar_item(0)
    repositorio.atualizar(tarefa)

    recuperada = repositorio.buscar_por_id(tarefa.id)

    assert recuperada.itens[0].feito is True
    assert recuperada.itens[1].feito is False

    print("TESTE marcação: APROVADO!")

    # Remover o segundo item
    tarefa.remover_item(1)
    repositorio.atualizar(tarefa)

    recuperada = repositorio.buscar_por_id(tarefa.id)

    assert len(recuperada.itens) == 2
    assert recuperada.itens[0].texto == "Classes"
    assert recuperada.itens[1].texto == "Polimorfismo"

    print("TESTE remoção de item: APROVADO!")

    # Concluir checklist
    tarefa.marcar_item(1)
    tarefa.concluir()

    repositorio.atualizar(tarefa)

    recuperada = repositorio.buscar_por_id(tarefa.id)

    assert recuperada.concluida is True
    assert all(item.feito for item in recuperada.itens)

    print("TESTE conclusão: APROVADO!")