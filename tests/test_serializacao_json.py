"""Teste de integração da serialização JSON com o SQLite.

Arquivo no projeto: tests/test_serializacao_json.py
Execução (raiz do projeto): python3 -m tests.test_serializacao_json

Requer GerenciadorTarefa.exportar_json(caminho) e
GerenciadorTarefa.importar_json(caminho) implementados.
"""

import json
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.tarefa_simples import TarefaSimples


def preparar_banco(caminho: Path) -> GerenciadorTarefa:
    conexao = conectar(str(caminho))
    try:
        schema = Path(__file__).resolve().parents[1] / "schema.sql"
        conexao.executescript(schema.read_text(encoding="utf-8"))
    finally:
        conexao.close()
    return GerenciadorTarefa(RepositorioSQLite(str(caminho)))


with TemporaryDirectory() as pasta:
    diretorio = Path(pasta)
    origem = preparar_banco(diretorio / "origem.db")
    destino = preparar_banco(diretorio / "destino.db")
    arquivo_json = diretorio / "tarefas_exportadas.json"
    vencimento = date.today() + timedelta(days=14)

    simples = origem.criar(TarefaSimples(
        None, "Estudar Python", "Revisar POO", Prioridade.ALTA, vencimento
    ))

    checklist = TarefaChecklist(
        None, "Preparar trabalho", "Conferir entregáveis", Prioridade.MEDIA, vencimento
    )
    checklist.adicionar_item("Escrever texto")
    checklist.adicionar_item("Revisar referências")
    checklist.marcar_item(0)
    checklist = origem.criar(checklist)

    recorrente = origem.criar(TarefaRecorr(
        None, "Praticar exercícios", "Rotina semanal", Prioridade.BAIXA,
        vencimento, Recorrencia("semanal", 2)
    ))

    origem.exportar_json(str(arquivo_json))
    assert arquivo_json.is_file(), "O arquivo JSON não foi criado."

    dados = json.loads(arquivo_json.read_text(encoding="utf-8"))
    assert isinstance(dados, list) and len(dados) == 3
    por_tipo = {item["tipo"]: item for item in dados}
    assert set(por_tipo) == {"TarefaSimples", "TarefaChecklist", "TarefaRecorr"}
    assert por_tipo["TarefaSimples"]["titulo"] == simples.titulo
    assert por_tipo["TarefaSimples"]["prioridade"] == "ALTA"
    assert por_tipo["TarefaSimples"]["data_vencimento"] == vencimento.isoformat()
    assert len(por_tipo["TarefaChecklist"]["itens"]) == 2
    assert por_tipo["TarefaChecklist"]["itens"][0] == {
        "texto": "Escrever texto", "feito": True
    }
    assert por_tipo["TarefaChecklist"]["itens"][1]["feito"] is False
    assert por_tipo["TarefaRecorr"]["recorrencia"] == {
        "frequencia": "semanal", "intervalo": 2
    }
    assert {item["id"] for item in dados} == {
        simples.id, checklist.id, recorrente.id
    }
    print("TESTE exportar_json(): APROVADO!")

    # Um registro pré-existente garante que os IDs do JSON não sejam reutilizados.
    existente = destino.criar(TarefaSimples(
        None, "Existente", "Não deve ser substituída", Prioridade.BAIXA, vencimento
    ))
    quantidade = destino.importar_json(str(arquivo_json))
    assert quantidade == 3, "A importação deve informar três tarefas importadas."

    todas = destino.listar()
    assert len(todas) == 4
    assert destino.buscar_por_id(existente.id).titulo == "Existente"
    importadas = [t for t in todas if t.id != existente.id]
    assert len(importadas) == 3
    assert all(t.id != existente.id for t in importadas)
    assert all(t.id is not None for t in importadas)
    assert len({t.id for t in todas}) == 4

    nova_simples = next(t for t in importadas if isinstance(t, TarefaSimples))
    nova_checklist = next(t for t in importadas if isinstance(t, TarefaChecklist))
    nova_recorrente = next(t for t in importadas if isinstance(t, TarefaRecorr))

    assert nova_simples.titulo == "Estudar Python"
    assert nova_simples.prioridade == Prioridade.ALTA
    assert nova_simples.data_vencimento == vencimento
    assert len(nova_checklist.itens) == 2
    assert nova_checklist.itens[0].texto == "Escrever texto"
    assert nova_checklist.itens[0].feito is True
    assert nova_checklist.itens[1].feito is False
    assert nova_recorrente.recorrencia.frequencia == "semanal"
    assert nova_recorrente.recorrencia.intervalo == 2
    print("TESTE importar_json(): APROVADO!")

    # Consulta novamente os dados, para conferir a persistência efetiva.
    reaberto = preparar_banco(diretorio / "destino.db")
    assert len(reaberto.listar()) == 4
    assert isinstance(reaberto.buscar_por_id(nova_checklist.id), TarefaChecklist)
    assert isinstance(reaberto.buscar_por_id(nova_recorrente.id), TarefaRecorr)
    print("TESTE persistência após importação: APROVADO!")

    # Entrada inválida não deve inserir registros.
    arquivo_invalido = diretorio / "invalido.json"
    arquivo_invalido.write_text('{"tipo": "TarefaSimples"}', encoding="utf-8")
    try:
        destino.importar_json(str(arquivo_invalido))
    except ValueError:
        pass
    else:
        raise AssertionError("Importação aceitou um objeto em vez de lista.")
    assert len(destino.listar()) == 4
    print("TESTE formato JSON inválido: APROVADO!")

print("TODOS OS TESTES DE SERIALIZAÇÃO: APROVADOS!")
