from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.prioridade import Prioridade
from package.tarefa_checklist import TarefaChecklist
from package.repositorio_sqlite import RepositorioSQLite


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_checklist.db")

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
        "Revisar programação orientada a objetos",
        Prioridade.ALTA,
        date(2026, 11, 20)
    )

    tarefa.adicionar_item("Estudar classes")
    tarefa.adicionar_item("Estudar herança")
    tarefa.adicionar_item("Estudar polimorfismo")

    tarefa.marcar_item(0)

    repositorio.adicionar(tarefa)

    assert tarefa.id is not None

    conexao = conectar(caminho_db)

    try:
        registros = conexao.execute(
            """
            SELECT posicao, texto, feito
            FROM itens_checklist
            WHERE tarefa_id = ?
            ORDER BY posicao
            """,
            (tarefa.id,)
        ).fetchall()

        print("Itens armazenados:", registros)

        assert registros == [
            (0, "Estudar classes", 1),
            (1, "Estudar herança", 0),
            (2, "Estudar polimorfismo", 0)
        ]

        print("TESTE INSERT CHECKLIST: APROVADO!")

    finally:
        conexao.close()

    # TESTE: RECONSTRUÇÃO DO CHECKLIST

    recuperada = repositorio.buscar_por_id(tarefa.id)

    assert isinstance(recuperada, TarefaChecklist)
    assert recuperada.id == tarefa.id
    assert recuperada.titulo == tarefa.titulo

    assert len(recuperada.itens) == 3

    assert recuperada.itens[0].texto == "Estudar classes"
    assert recuperada.itens[0].feito is True

    assert recuperada.itens[1].texto == "Estudar herança"
    assert recuperada.itens[1].feito is False

    assert recuperada.itens[2].texto == "Estudar polimorfismo"
    assert recuperada.itens[2].feito is False

    print("TESTE buscar_por_id() CHECKLIST: APROVADO!")