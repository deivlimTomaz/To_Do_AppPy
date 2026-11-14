from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_simples import TarefaSimples
from package.prioridade import Prioridade


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_update.db")

    # Inicializa as tabelas
    conexao = conectar(caminho_db)

    try:
        schema = Path("schema.sql").read_text(encoding="utf-8")
        conexao.executescript(schema)
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    # 1. Cadastrar
    tarefa = TarefaSimples(
        None,
        "Estudar Python",
        "Revisar POO",
        Prioridade.ALTA,
        date(2026, 11, 17)
    )

    repositorio.adicionar(tarefa)
    id_original = tarefa.id

    # 2. Modificar o objeto
    tarefa.editar(
        "Estudar SQLite",
        "Aprender UPDATE",
        Prioridade.MEDIA,
        date(2026, 11, 20)
    )

    tarefa.concluir()

    # 3. Persistir as alterações
    repositorio.atualizar(tarefa)

    # 4. Recuperar novamente do banco
    recuperada = repositorio.buscar_por_id(id_original)

    assert recuperada is not None
    assert recuperada.id == id_original
    assert recuperada.titulo == "Estudar SQLite"
    assert recuperada.descricao == "Aprender UPDATE"
    assert recuperada.prioridade == Prioridade.MEDIA
    assert recuperada.data_vencimento == date(2026, 11, 20)
    assert recuperada.concluida is True

    print("TESTE atualizar(): APROVADO!")

    # TESTE: ATUALIZAÇÃO DA TAREFA INEXISTENTE -> Verifica tratamento de exceções

    tarefa_inexistente = TarefaSimples(
        9999,
        "Tarefa inexistente",
        "Teste de erro",
        Prioridade.BAIXA,
        date(2026, 11, 20)
    )

    try:
        repositorio.atualizar(tarefa_inexistente)
    except ValueError:
        print("TESTE ID inexistente: APROVADO!")
    else:
        raise AssertionError(
            "O método deveria lançar ValueError para um ID inexistente."
        )