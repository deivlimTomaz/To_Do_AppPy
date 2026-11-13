
from datetime import date
from package.repositorio import Repositorio
from package.tarefa import Tarefa
from package.tarefa_simples import TarefaSimples
from package.conexao import conectar
from package.prioridade import Prioridade

class RepositorioSQLite(Repositorio):
    
    def __init__(self, caminho_db: str = "tarefas.db"):
        self._caminho_db = caminho_db

    def adicionar(self, tarefa: Tarefa) -> Tarefa:

        if not isinstance(tarefa, TarefaSimples):
            raise NotImplementedError("Somente TarefaSimples é suportada nesta etapa.")
        
        conexao = conectar(self._caminho_db)

        try:
            cursor = conexao.cursor()

            tipo_tarefa = type(tarefa).__name__
            dados = (
                tipo_tarefa,
                tarefa.titulo,
                tarefa.descricao,
                tarefa.prioridade.name,
                tarefa.data_vencimento.isoformat(),
                int(tarefa.concluida),
            )

            sql = """INSERT INTO tarefas (
                        tipo,
                        titulo,
                        descricao,
                        prioridade,
                        data_vencimento,
                        concluida
                    )
                    VALUES (?, ?, ?, ?, ?, ?);
                    """
            cursor.execute(sql, dados)

            novo_id = cursor.lastrowid

            if novo_id is None:
                raise RuntimeError("Não foi possível recuper o ID gerado.")

            conexao.commit()
            tarefa.atribuir_id(novo_id)

            return tarefa

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()        
        

    def buscar_por_id(self, id: int) -> Tarefa | None:
        conexao = conectar(self._caminho_db)

        try:
            cursor = conexao.cursor()

            cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id,))
            linha = cursor.fetchone()

            if linha is None:
                return None

            if linha[1] != "TarefaSimples":
                raise NotImplementedError(
                    "A reconstrução deste tipo de tarefa ainda não foi implementada."
                )

            tarefa = TarefaSimples(
                linha[0],
                linha[2],
                linha[3],
                Prioridade[linha[4]],
                date.fromisoformat(linha[5])
            )

            if bool(linha[6]):
                tarefa.concluir()

            return tarefa
        
        finally:
            conexao.close()


    def listar(self) -> list[Tarefa]:
        conexao = conectar(self._caminho_db)

        try:
            cursor = conexao.cursor()

            cursor.execute("SELECT id FROM tarefas ORDER BY id;")
            linhas = cursor.fetchall()

        finally:
            conexao.close()

        tarefas = []

        for linha in linhas:
            id_tarefa = linha[0]

            tarefa = self.buscar_por_id(id_tarefa)

            if tarefa is None:
                raise RuntimeError(f"A tarefa de ID {id_tarefa} não pôde ser recuperada.")

            tarefas.append(tarefa)

        return tarefas


    def atualizar(self, tarefa: Tarefa) -> None:
        raise NotImplementedError

    def remover(self, id: int) -> None:
        raise NotImplementedError
