from package.conexao import conectar
import sqlite3

if __name__ == "__main__":

    # Chama o método conectar()
    # A função deve retornar o objeto de conexão já com o PRAGMA ativado
    conexao = conectar("tarefas.db")

    # Criação de um cursor para executar as consultas SQL no db
    cursor = conexao.cursor()

    try:

        # Processo de verificação de versão do SQLite
        cursor.execute("SELECT sqlite_version();")

        versao_sqlite = cursor.fetchone()[0]

        print(f"Versão do SQL instalada: {versao_sqlite}")

        # Execução do PRAGMA foreign_keys
        cursor.execute("PRAGMA foreign_keys;")
        status_fk = cursor.fetchone()[0]

        if status_fk == 1:
            print(
                f"Chaves estrangeiras ativas! Retorna: {status_fk}"
            )
        else:
            print(
                f"Chaves estrangeiras DESATIVADAS! Retorna: {status_fk}"
            )

    except Exception as erro:
        print(f"Ocorrência de falha durante a execução: {erro}")

    finally:
        cursor.close()
        conexao.close()
        print("\nConexão fechada com sucesso. Teste finalizado!")