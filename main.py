from pathlib import Path

from package.menu import Menu # Interação com o usuário
from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa # Operações e regras de negócio
from package.repositorio_sqlite import RepositorioSQLite # Acesso ao banco de dados

if __name__ == "__main__":

    caminho_db = "tarefas.db"

    conexao = conectar(caminho_db)

    try:

        schema = Path(__file__).resolve().parent / "schema.sql"
        conexao.executescript(schema.read_text(encoding="utf-8"))

    finally:
        conexao.close()

    repositorio = RepositorioSQLite(caminho_db)

    gerenciador = GerenciadorTarefa(repositorio)

    sistema = Menu(gerenciador, repositorio)

    sistema.mostrar_menu()
