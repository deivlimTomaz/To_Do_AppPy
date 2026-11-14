
from datetime import date
from package.repositorio import Repositorio
from package.tarefa import Tarefa
from package.tarefa_checklist import TarefaChecklist
from package.item_checklist import ItemChecklist
from package.tarefa_simples import TarefaSimples
from package.conexao import conectar
from package.prioridade import Prioridade

class RepositorioSQLite(Repositorio):
    
    def __init__(self, caminho_db: str = "tarefas.db"):
        self._caminho_db = caminho_db

    def adicionar(self, tarefa: Tarefa) -> Tarefa:

        if not isinstance(tarefa, (TarefaSimples, TarefaChecklist)):
            raise TypeError("Tipo de tarefa ainda não suportado.")

        if tarefa.id is not None:
            raise ValueError("A tarefa já possui um ID.")

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
                raise RuntimeError("Não foi possível recuperar o ID gerado.")

            if isinstance(tarefa, TarefaChecklist):

                sql_checklist = """INSERT INTO itens_checklist (
                                        tarefa_id,
                                        posicao,
                                        texto,
                                        feito
                                )
                                VALUES (?, ?, ?, ?);"""

                for posicao, item in enumerate(tarefa.itens):
                    dados_item = (
                        novo_id,
                        posicao,
                        item.texto,
                        int(item.feito)
                    ) 

                    conexao.execute(sql_checklist, dados_item)

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

            if linha[1] == "TarefaSimples":

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

            if linha[1] == "TarefaChecklist":

                itens_checklist = """SELECT texto, feito
                                    FROM itens_checklist
                                    WHERE tarefa_id = ?
                                    ORDER BY posicao;"""

                dados = {
                    "id": linha[0],
                    "tipo": linha[1],
                    "titulo": linha[2],
                    "descricao": linha[3],
                    "prioridade": linha[4],
                    "data_vencimento": linha[5],
                    "concluida": bool(linha[6]),
                    "itens": []
                }

                cursor.execute(itens_checklist, (id,))

                linhas_itens = cursor.fetchall()

                for linha_item in linhas_itens: # Aproveitamento de desserialização de objetos
                    item = {
                        "texto": linha_item[0],
                        "feito": bool(linha_item[1])
                    }

                    dados["itens"].append(item)

                return TarefaChecklist.de_dict(dados)

            raise NotImplementedError(f"Reconstrução não implementada para o tipo: {linha[1]}")
        
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

        if not isinstance(tarefa, (TarefaSimples, TarefaChecklist)):
            raise TypeError("Tipo de tarefa ainda não suportado")

        if tarefa.id is None:
            raise ValueError("O ID da tarefa não existe")

        
        conexao = conectar(self._caminho_db)

        try:
            cursor = conexao.cursor()

            dados = (
                tarefa.titulo,
                tarefa.descricao,
                tarefa.prioridade.name,
                tarefa.data_vencimento.isoformat(),
                int(tarefa.concluida),
                tarefa.id,
                type(tarefa).__name__
            )

            sql = """
                UPDATE tarefas
                SET titulo = ?,
                    descricao = ?,
                    prioridade = ?,
                    data_vencimento = ?,
                    concluida = ?
                WHERE id = ? AND tipo = ?;"""
            
            cursor.execute(sql, dados)

            if cursor.rowcount == 0:
                raise ValueError("Tarefa não foi encontrada")

            if isinstance(tarefa, TarefaChecklist):
                remover_itens_ant = """
                    DELETE FROM itens_checklist
                    WHERE tarefa_id = ?;"""

                cursor.execute(remover_itens_ant, (tarefa.id,))
                    
                inserir_itens_atuais = """
                    INSERT INTO itens_checklist (
                        tarefa_id,
                        posicao,
                        texto,
                        feito
                    )
                VALUES (?, ?, ?, ?);"""

                for posicao, item in enumerate(tarefa.itens):
                    dados_item = (
                        tarefa.id,
                        posicao,
                        item.texto,
                        int(item.feito)
                    )

                    cursor.execute(inserir_itens_atuais, dados_item)


            conexao.commit() # Em caso de sucesso, atualiza todos os dados.

        except Exception:
            conexao.rollback() # Desfaz todas as modificações feitas em caso de erro
            raise

        finally:
            conexao.close()

            
    def remover(self, id: int) -> None:

        if not isinstance(id, int) or isinstance(id, bool):
            raise TypeError("O ID deve ser um inteiro")

        conexao = conectar(self._caminho_db)

        try:
            cursor = conexao.cursor()

            cursor.execute("DELETE FROM tarefas WHERE id = ?;", (id,))

            if cursor.rowcount == 0:
                raise ValueError("Tarefa não foi encontrada")

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()