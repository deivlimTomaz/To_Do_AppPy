from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.tarefa_recorr import TarefaRecorr
from package.repositorio_sqlite import RepositorioSQLite


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_recorrencia.db")

    conexao = conectar(caminho_db)

    try:
        sql = Path("schema.sql").read_text(encoding="utf-8")
        conexao.executescript(sql)
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    recorrencia = Recorrencia("semanal", 2)

    tarefa = TarefaRecorr(
        None,
        "Estudar Python",
        "Revisar orientação a objetos",
        Prioridade.ALTA,
        date(2026, 11, 20),
        recorrencia
    )

    repositorio.adicionar(tarefa)

    assert tarefa.id is not None

    conexao = conectar(caminho_db)

    try:
        registro = conexao.execute(
            """
            SELECT frequencia, intervalo
            FROM recorrencias
            WHERE tarefa_id = ?
            """,
            (tarefa.id,)
        ).fetchone()

        assert registro == ("semanal", 2)

        print("TESTE INSERT RECORRÊNCIA: APROVADO!")
        
        print("============================================================================")
        registro_tarefa = conexao.execute(
            "SELECT tipo FROM tarefas WHERE id = ?",
            (tarefa.id,)
        ).fetchone()

        assert registro_tarefa == ("TarefaRecorr",)

        print("TESTE TIPO DA TAREFA: APROVADO!")

        print("============================================================================")

        # TESTE: RECUPERAR TAREFA RECORRENTE

        recuperada = repositorio.buscar_por_id(tarefa.id)

        assert isinstance(recuperada, TarefaRecorr)
        assert recuperada.id == tarefa.id
        assert recuperada.titulo == tarefa.titulo
        assert recuperada.prioridade == tarefa.prioridade
        assert recuperada.data_vencimento == tarefa.data_vencimento

        assert recuperada.recorrencia.frequencia == "semanal"
        assert recuperada.recorrencia.intervalo == 2

        assert recuperada.concluida is False

        print("TESTE buscar_por_id() RECORRENTE: APROVADO!")


    finally:
        conexao.close()
