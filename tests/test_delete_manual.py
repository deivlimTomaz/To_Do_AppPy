from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_simples import TarefaSimples
from package.prioridade import Prioridade


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_delete.db")

    conexao = conectar(caminho_db)

    try:
        sql = Path("schema.sql").read_text(encoding="utf-8")
        conexao.executescript(sql)
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    tarefa = TarefaSimples(
        None,
        "Teste de exclusão",
        "Verificar DELETE",
        Prioridade.MEDIA,
        date(2026, 11, 20)
    )

    repositorio.adicionar(tarefa)

    id_tarefa = tarefa.id

    assert repositorio.buscar_por_id(id_tarefa) is not None

    # Excluir tarefa
    repositorio.remover(id_tarefa)

    # Confirmar exclusão
    assert repositorio.buscar_por_id(id_tarefa) is None
    assert repositorio.listar() == []

    print("TESTE remover(): APROVADO!")

    # Tentar excluir novamente
    try:
        repositorio.remover(id_tarefa)
    except ValueError:
        print("TESTE ID inexistente: APROVADO!")
    else:
        raise AssertionError(
            "O método deveria lançar ValueError."
        )

    # TESTE ID NEGATIVO

    try:
        repositorio.remover(-5)
    except ValueError:
        print("TESTE ID negativo: APROVADO!")
    else:
        raise AssertionError("ID negativo deveria gerar ValueError")

    # TESTE ID BOOLEANO
    try:
        repositorio.remover(True)
    except TypeError:
        print("TESTE ID booleano: APROVADO!")
    else:
        raise AssertionError("ID booleano deveria gerar TypeError")

    # TESTE ID STRING
    try:
        repositorio.remover("abc")
    except TypeError:
        print("TESTE ID string: APROVADO!")
    else:
        raise AssertionError("ID string deveria gerar TypeError")