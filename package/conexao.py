import sqlite3

def conectar(caminho: str = "tarefas.db") -> sqlite3.Connection:

    # Criar conexão com o arquivo de banco de dados
    conexao = sqlite3.connect(caminho)

    # Gerar chaves estrangeiras
    conexao.execute("PRAGMA foreign_keys = ON;")

    return conexao