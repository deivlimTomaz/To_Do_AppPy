from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.repositorio_sqlite import RepositorioSQLite
from package.gerenciador_tarefa import GerenciadorTarefa
from package.tarefa_simples import TarefaSimples
from package.prioridade import Prioridade


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_gerenciador.db")

    # Inicializar as tabelas
    conexao = conectar(caminho_db)

    try:
        schema = Path("schema.sql").read_text(encoding="utf-8")
        conexao.executescript(schema)
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)
    gerenciador = GerenciadorTarefa(repositorio)

    # TESTE 1: Criar
    tarefa = TarefaSimples(
        None,
        "Estudar SQLite",
        "Testar o gerenciador",
        Prioridade.ALTA,
        date.today() + timedelta(days=7)
    )

    criada = gerenciador.criar(tarefa)

    assert criada.id is not None
    assert criada.id == tarefa.id

    print("TESTE criar(): APROVADO!")

    # TESTE 2: Buscar
    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert recuperada.id == tarefa.id
    assert recuperada.titulo == tarefa.titulo

    print("TESTE buscar_por_id(): APROVADO!")

    # TESTE 3: Listar
    tarefas = gerenciador.listar()

    assert len(tarefas) == 1
    assert tarefas[0].id == tarefa.id

    print("TESTE listar(): APROVADO!")

    # TESTE 4: Filtrar
    filtradas = gerenciador.filtrar(Prioridade.ALTA)

    assert len(filtradas) == 1
    assert filtradas[0].id == tarefa.id

    assert gerenciador.filtrar(Prioridade.BAIXA) == []

    print("TESTE filtrar(): APROVADO!")

    # TESTE 5: CONCLUIR TAREFA

    gerenciador.concluir(tarefa)

    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert recuperada.concluida is True

    print("TESTE concluir(): APROVADO!")

    # TESTE: REABRIR TAREFA

    gerenciador.reabrir(tarefa)

    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert recuperada.concluida is False

    print("TESTE reabrir(): APROVADO!")

    # TESTE 6: Excluir
    gerenciador.excluir(tarefa)

    assert gerenciador.listar() == []

    try:
        gerenciador.buscar_por_id(tarefa.id)
    except ValueError:
        print("TESTE excluir(): APROVADO!")
    else:
        raise AssertionError("A tarefa excluída ainda foi encontrada.")
