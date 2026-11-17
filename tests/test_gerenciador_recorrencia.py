from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_recorr import TarefaRecorr
from package.tarefa_simples import TarefaSimples


with TemporaryDirectory() as pasta:
    caminho_db = str(Path(pasta) / "teste_gerenciador_recorrencia.db")

    # Execute este arquivo a partir da raiz do projeto.
    schema = Path("schema.sql").read_text(encoding="utf-8")
    conexao = conectar(caminho_db)
    try:
        conexao.executescript(schema)
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)
    gerenciador = GerenciadorTarefa(repositorio)

    vencimento = date.today() + timedelta(days=1)
    original = TarefaRecorr(
        None,
        "Estudar Python",
        "Revisar programação orientada a objetos",
        Prioridade.ALTA,
        vencimento,
        Recorrencia("semanal", 1),
    )

    # TESTE 1: cadastro da ocorrência original
    gerenciador.criar(original)
    assert original.id is not None
    id_original = original.id
    assert isinstance(gerenciador.buscar_por_id(id_original), TarefaRecorr)
    print("TESTE cadastrar recorrência original: APROVADO!")

    # TESTE 2: não pode gerar próxima ocorrência de tarefa pendente
    try:
        gerenciador.gerar_proxima_recorrencia(id_original)
    except ValueError:
        pass
    else:
        raise AssertionError("Foi possível gerar uma recorrência sem concluir a original.")
    assert len(gerenciador.listar()) == 1
    print("TESTE impedir geração de recorrência pendente: APROVADO!")

    # TESTE 3: concluir e persistir a ocorrência original
    gerenciador.concluir(original)
    original_recuperada = gerenciador.buscar_por_id(id_original)
    assert original_recuperada.concluida is True
    print("TESTE concluir ocorrência original: APROVADO!")

    # TESTE 4: gerar próxima ocorrência com novo ID e vencimento semanal
    proxima = gerenciador.gerar_proxima_recorrencia(id_original)
    assert isinstance(proxima, TarefaRecorr)
    assert proxima.id is not None
    assert proxima.id != id_original
    assert proxima.data_vencimento == vencimento + timedelta(days=7)
    assert proxima.concluida is False
    assert proxima.recorrencia.frequencia == "semanal"
    assert proxima.recorrencia.intervalo == 1
    print("TESTE gerar próxima recorrência: APROVADO!")

    # TESTE 5: confirmar os dois registros consultando novamente o banco
    original_no_banco = gerenciador.buscar_por_id(id_original)
    proxima_no_banco = gerenciador.buscar_por_id(proxima.id)
    assert original_no_banco.concluida is True
    assert proxima_no_banco.concluida is False
    assert proxima_no_banco.data_vencimento == vencimento + timedelta(days=7)
    assert proxima_no_banco.recorrencia.frequencia == "semanal"
    assert proxima_no_banco.recorrencia.intervalo == 1
    assert len(gerenciador.listar()) == 2
    print("TESTE persistência das duas ocorrências: APROVADO!")

    # TESTE 6: recusar geração a partir de uma tarefa que não é recorrente
    simples = TarefaSimples(
        None, "Tarefa simples", "Sem recorrência", Prioridade.MEDIA, vencimento
    )
    gerenciador.criar(simples)
    try:
        gerenciador.gerar_proxima_recorrencia(simples.id)
    except TypeError:
        pass
    else:
        raise AssertionError("Foi possível gerar recorrência a partir de tarefa simples.")
    print("TESTE recusar tipo não recorrente: APROVADO!")

    print("\nTODOS OS TESTES DE RECORRÊNCIA DO GERENCIADOR PASSARAM!")

