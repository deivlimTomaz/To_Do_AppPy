"""Inicia a interface gráfica usando o mesmo SQLite do terminal."""
from pathlib import Path

from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.repositorio_sqlite import RepositorioSQLite
from interface.app import App


def main():
    pasta_projeto = Path(__file__).resolve().parent
    caminho_db = pasta_projeto / "tarefas.db"
    caminho_schema = pasta_projeto / "schema.sql"

    conexao = conectar(str(caminho_db))
    try:
        conexao.executescript(caminho_schema.read_text(encoding="utf-8"))
    finally:
        conexao.close()

    repositorio = RepositorioSQLite(str(caminho_db))
    gerenciador = GerenciadorTarefa(repositorio)

    app = App(gerenciador)
    app.executar()


if __name__ == "__main__":
    main()
