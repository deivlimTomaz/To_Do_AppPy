"""Testa leitura, seleção e apresentação dos dados, sem abrir uma janela."""
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.tarefa_simples import TarefaSimples
from interface.tarefas_view import filtrar_tarefas, resumo_tarefa


class TestInterfaceIntegracao(unittest.TestCase):
    def setUp(self):
        self.pasta_temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta_temporaria.cleanup)
        caminho_db = str(Path(self.pasta_temporaria.name) / "teste_interface.db")
        schema = Path(__file__).resolve().parents[1] / "schema.sql"
        conexao = conectar(caminho_db)
        try:
            conexao.executescript(schema.read_text(encoding="utf-8"))
        finally:
            conexao.close()
        self.gerenciador = GerenciadorTarefa(RepositorioSQLite(caminho_db))

    def test_listar_e_filtrar_tipos(self):
        vencimento = date.today() + timedelta(days=5)
        self.gerenciador.criar(
            TarefaSimples(None, "Simples", "Descrição", Prioridade.ALTA, vencimento)
        )
        self.gerenciador.criar(
            TarefaChecklist(None, "Checklist", "Descrição", Prioridade.MEDIA, vencimento)
        )
        self.gerenciador.criar(
            TarefaRecorr(
                None, "Recorrente", "Descrição", Prioridade.BAIXA,
                vencimento, Recorrencia("semanal", 1)
            )
        )
        tarefas = self.gerenciador.listar()
        self.assertEqual(len(filtrar_tarefas(tarefas, "Tarefas")), 3)
        self.assertEqual(len(filtrar_tarefas(tarefas, "Checklists")), 1)
        self.assertEqual(len(filtrar_tarefas(tarefas, "Recorrentes")), 1)

    def test_campos_do_cartao(self):
        vencimento = date.today() + timedelta(days=5)
        tarefa = self.gerenciador.criar(
            TarefaSimples(None, "Estudar Python", "Descrição", Prioridade.ALTA, vencimento)
        )
        tarefa_lida = self.gerenciador.buscar_por_id(tarefa.id)
        dados = resumo_tarefa(tarefa_lida)
        self.assertEqual(dados["id"], tarefa.id)
        self.assertEqual(dados["titulo"], "Estudar Python")
        self.assertEqual(dados["prioridade"], "Alta")
        self.assertEqual(dados["vencimento"], vencimento.strftime("%d/%m/%Y"))
        self.assertFalse(dados["concluida"])
        self.assertFalse(dados["atrasada"])

    def test_estado_atualizado_apos_concluir(self):
        vencimento = date.today() + timedelta(days=5)
        tarefa = self.gerenciador.criar(
            TarefaSimples(None, "Concluir", "Descrição", Prioridade.BAIXA, vencimento)
        )
        self.gerenciador.concluir(tarefa)
        nova_leitura = self.gerenciador.listar()
        self.assertTrue(resumo_tarefa(nova_leitura[0])["concluida"])

    def test_lista_vazia(self):
        self.assertEqual(filtrar_tarefas(self.gerenciador.listar(), "Tarefas"), [])


if __name__ == "__main__":
    unittest.main()
