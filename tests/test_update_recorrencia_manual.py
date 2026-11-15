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
        schema = Path("schema.sql").read_text(encoding="utf-8")
        conexao.executescript(schema)
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    tarefa = TarefaRecorr(
        None,
        "Estudar Python",
        "Revisar POO",
        Prioridade.ALTA,
        date(2026, 11, 20),
        Recorrencia("semanal", 1)
    )

    repositorio.adicionar(tarefa)

    # Modificar dados comuns
    tarefa.editar(
        "Estudar SQLite",
        "Revisar persistência",
        Prioridade.MEDIA,
        date(2026, 11, 25)
    )

    # Modificar configuração da recorrência
    tarefa.recorrencia.frequencia = "mensal"
    tarefa.recorrencia.intervalo = 2

    # Concluir a tarefa
    tarefa.concluir()

    # Persistir alterações
    repositorio.atualizar(tarefa)

    # Recuperar novamente
    recuperada = repositorio.buscar_por_id(tarefa.id)

    assert isinstance(recuperada, TarefaRecorr)
    assert recuperada.titulo == "Estudar SQLite"
    assert recuperada.prioridade == Prioridade.MEDIA
    assert recuperada.recorrencia.frequencia == "mensal"
    assert recuperada.recorrencia.intervalo == 2
    assert recuperada.concluida is True

    print("TESTE atualizar() RECORRENTE: APROVADO!")

    # TESTE: INTERVALO IGUAL AO ID DA TAREFA

    tarefa.recorrencia.intervalo = tarefa.id

    repositorio.atualizar(tarefa)

    recuperada = repositorio.buscar_por_id(tarefa.id)

    assert recuperada.recorrencia.intervalo == tarefa.id

    print("TESTE parâmetros repetidos: APROVADO!")  
