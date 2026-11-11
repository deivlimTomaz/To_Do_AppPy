from pathlib import Path
from package.conexao import conectar

raiz = Path(__file__).resolve().parents[1]
caminho_schema = raiz / "schema.sql"

conexao = conectar(str(raiz / "teste_schema.db"))

try:
    sql = caminho_schema.read_text(encoding="utf-8")
    conexao.executescript(sql)

    cursor = conexao.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' ORDER BY name"
    )

    for tabela in cursor.fetchall():
        print(tabela[0])

finally:
    conexao.close()
