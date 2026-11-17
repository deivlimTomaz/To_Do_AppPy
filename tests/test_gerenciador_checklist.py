from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.repositorio_sqlite import RepositorioSQLite
from package.gerenciador_tarefa import GerenciadorTarefa
from package.tarefa_checklist import TarefaChecklist
from package.prioridade import Prioridade


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_checklist.db")

    conexao = conectar(caminho_db)
    try:
        conexao.executescript(
            Path("schema.sql").read_text(encoding="utf-8")
        )
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)
    gerenciador = GerenciadorTarefa(repositorio)

    tarefa = TarefaChecklist(
        None,
        "Preparar apresentação",
        "Checklist de atividades",
        Prioridade.ALTA,
        date.today() + timedelta(days=7)
    )

    gerenciador.criar(tarefa)

    # TESTE 1: ADICIONAR ITENS
    gerenciador.adicionar_item(tarefa.id, "Criar slides")
    gerenciador.adicionar_item(tarefa.id, "Revisar conteúdo")

    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert len(recuperada.itens) == 2
    assert recuperada.itens[0].texto == "Criar slides"
    assert recuperada.itens[1].texto == "Revisar conteúdo"

    print("TESTE adicionar_item(): APROVADO!")

    # TESTE 2: MARCAR ITEM
    gerenciador.marcar_item(tarefa.id, 0)

    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert recuperada.itens[0].feito is True

    print("TESTE marcar_item(): APROVADO!")

    # TESTE 3: DESMARCAR ITEM
    gerenciador.desmarcar_item(tarefa.id, 0)

    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert recuperada.itens[0].feito is False

    print("TESTE desmarcar_item(): APROVADO!")

    # TESTE 4: REMOVER ITEM
    gerenciador.remover_item(tarefa.id, 0)

    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert len(recuperada.itens) == 1
    assert recuperada.itens[0].texto == "Revisar conteúdo"

    print("TESTE remover_item(): APROVADO!")

    # TESTE 5: CONSISTÊNCIA DA CONCLUSÃO

    gerenciador.marcar_item(tarefa.id, 0)

    gerenciador.concluir(tarefa)

    recuperada = gerenciador.buscar_por_id(tarefa.id)
    assert recuperada.concluida is True

    # Não é permitido desmarcar uma tarefa concluída.
    try:
        gerenciador.desmarcar_item(tarefa.id, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("O checklist permitiu alterar uma tarefa concluída.")

    # A tentativa inválida não deve alterar os dados.
    recuperada = gerenciador.buscar_por_id(tarefa.id)
    assert recuperada.concluida is True
    assert recuperada.itens[0].feito is True

    # Reabrir antes de modificar.
    gerenciador.reabrir(tarefa)
    gerenciador.desmarcar_item(tarefa.id, 0)

    recuperada = gerenciador.buscar_por_id(tarefa.id)

    assert recuperada.itens[0].feito is False
    assert recuperada.concluida is False

    print("TESTE consistência da conclusão: APROVADO!")