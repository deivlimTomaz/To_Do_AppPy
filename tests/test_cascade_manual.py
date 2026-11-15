from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.repositorio_sqlite import RepositorioSQLite


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_cascade.db")

    conexao = conectar(caminho_db)
    try:
        conexao.executescript(
            Path("schema.sql").read_text(encoding="utf-8")
        )
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    checklist = TarefaChecklist(
        None, "Checklist", "Teste de exclusão",
        Prioridade.MEDIA, date(2026, 11, 20)
    )
    checklist.adicionar_item("Item 1")
    checklist.adicionar_item("Item 2")

    recorrente = TarefaRecorr(
        None, "Recorrente", "Teste de exclusão",
        Prioridade.ALTA, date(2026, 11, 20),
        Recorrencia("semanal", 1)
    )

    repositorio.adicionar(checklist)
    repositorio.adicionar(recorrente)

    repositorio.remover(checklist.id)
    repositorio.remover(recorrente.id)

    conexao = conectar(caminho_db)
    try:
        itens = conexao.execute(
            "SELECT COUNT(*) FROM itens_checklist"
        ).fetchone()[0]

        recorrencias = conexao.execute(
            "SELECT COUNT(*) FROM recorrencias"
        ).fetchone()[0]

        tarefas = conexao.execute(
            "SELECT COUNT(*) FROM tarefas"
        ).fetchone()[0]

        assert itens == 0
        assert recorrencias == 0
        assert tarefas == 0

        print("TESTE EXCLUSÃO EM CASCATA: APROVADO!")
    finally:
        conexao.close()
