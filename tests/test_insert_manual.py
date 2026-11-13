from datetime import date
from pathlib import Path

from package.conexao import conectar
from package.prioridade import Prioridade
from package.tarefa_simples import TarefaSimples
from package.repositorio_sqlite import RepositorioSQLite

caminho_db = Path("teste_id.db")

conexao = conectar(str(caminho_db))

try:
    # Leitura de conteúdo do SQL externo e carregamento como texto dentro de uma variável
    # para executar no banco de dados

    sql = Path("schema.sql").read_text(encoding="utf-8")
    conexao.executescript(sql)

finally:
    conexao.close()

# Inicializar o repositório
repositorio = RepositorioSQLite(str(caminho_db))

tarefa = TarefaSimples (
    None,
    "Estudar SQLite",
    "Testar geração automática de ID",
    Prioridade.ALTA,
    date(2026, 11, 17)
)

print("ID antes:", tarefa.id)

repositorio.adicionar(tarefa)

print("ID depois:", tarefa.id)

conexao = conectar(str(caminho_db))

try:
    cursor = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (tarefa.id,)
    )

    resultado = cursor.fetchone()

    print("Registro no SQLite:", resultado)

    assert tarefa.id is not None
    assert resultado is not None
    assert resultado[0] == tarefa.id

    print("TESTE APROVADO!\n")

finally:
    conexao.close()

print("=" * 80)

# TESTE: BUSCAR TAREFA POR ID

tarefa_recuperada = repositorio.buscar_por_id(tarefa.id)

assert tarefa_recuperada is not None
assert isinstance(tarefa_recuperada, TarefaSimples)

assert tarefa_recuperada.id == tarefa.id
assert tarefa_recuperada.titulo == tarefa.titulo
assert tarefa_recuperada.descricao == tarefa.descricao
assert tarefa_recuperada.prioridade == tarefa.prioridade
assert tarefa_recuperada.data_vencimento == tarefa.data_vencimento
assert tarefa_recuperada.concluida == tarefa.concluida

print("TESTE buscar_por_id(): APROVADO!")

# TESTE: ID INEXISTENTE
assert repositorio.buscar_por_id(-1) is None

print("TESTE ID inexistente: APROVADO!\n")

print("=" * 80)

# TESTE: LISTAR TAREFAS

tarefas = repositorio.listar()

assert isinstance(tarefas, list)
assert len(tarefas) > 0

for t in tarefas:
    assert isinstance(t, TarefaSimples)
    print(f"ID: {t.id} | Título: {t.titulo}")

print("TESTE listar(): APROVADO!")