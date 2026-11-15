from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.tarefa_recorr import TarefaRecorr
from package.repositorio_sqlite import RepositorioSQLite


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_proxima.db")

    conexao = conectar(caminho_db)
    try:
        conexao.executescript(
            Path("schema.sql").read_text(encoding="utf-8")
        )
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    original = TarefaRecorr(
        None,
        "Estudar Python",
        "Revisar POO",
        Prioridade.ALTA,
        date(2026, 11, 20),
        Recorrencia("semanal", 1)
    )

    repositorio.adicionar(original)
    original_id = original.id

    original.concluir()
    repositorio.atualizar(original)

    proxima = original.gerar_proxima()

    assert proxima.id is None
    assert proxima.data_vencimento > original.data_vencimento
    assert proxima.concluida is False

    repositorio.adicionar(proxima)

    assert proxima.id is not None
    assert proxima.id != original_id

    recuperada = repositorio.buscar_por_id(proxima.id)

    assert isinstance(recuperada, TarefaRecorr)
    assert recuperada.recorrencia.frequencia == "semanal"
    assert recuperada.recorrencia.intervalo == 1
    assert recuperada.concluida is False

    assert len(repositorio.listar()) == 2

    print("TESTE GERAÇÃO DE RECORRÊNCIA: APROVADO!")
    print(f"ID original: {original_id}")
    print(f"ID da próxima ocorrência: {proxima.id}")
    print(f"Próximo vencimento: {proxima.data_vencimento}")
