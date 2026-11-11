from datetime import date

from package.conexao import conectar
from package.prioridade import Prioridade
from package.tarefa_simples import TarefaSimples
from package.repositorio_sqlite import RepositorioSQLite


repositorio = RepositorioSQLite("teste_schema.db")

tarefa = TarefaSimples(
    1,
    "Estudar SQLite",
    "Praticar comandos INSERT",
    Prioridade.ALTA,
    date(2026, 11, 17)
)

repositorio.adicionar(tarefa)

conexao = conectar("teste_schema.db")

try:
    cursor = conexao.execute("SELECT * FROM tarefas WHERE id = ?", (1,))
    print(cursor.fetchone())
finally:
    conexao.close()