from package.repositorio import Repositorio
from package.tarefa import Tarefa
from package.tarefa_simples import TarefaSimples
from package.conexao import conectar

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
                tarefa.id,
                tipo_tarefa,
                tarefa.titulo,
                tarefa.descricao,
                tarefa.prioridade.name,
                tarefa.data_vencimento.isoformat(),
                int(tarefa.concluida),
            )

            sql = """INSERT INTO tarefas (
                        id,
                        tipo,
                        titulo,
                        descricao,
                        prioridade,
                        data_vencimento,
                        concluida
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """
            cursor.execute(sql, dados)

            conexao.commit()

            return tarefa

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()        
        

    def buscar_por_id(self, id: int) -> Tarefa | None:
        raise NotImplementedError

    def listar(self) -> list[Tarefa]:
        raise NotImplementedError

    def atualizar(self, tarefa: Tarefa) -> None:
        raise NotImplementedError

    def remover(self, id: int) -> None:
        raise NotImplementedError