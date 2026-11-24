"""Testes do gerenciamento de tarefas simples usando banco temporário."""
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from interface.cadastro import criar_tarefa_simples
from interface.gerenciamento import (buscar_simples, editar_simples,
    alternar_conclusao_simples, excluir_simples)
from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.prioridade import Prioridade
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_checklist import TarefaChecklist


class TestGerenciamentoInterface(unittest.TestCase):
    def setUp(self):
        temporario = tempfile.TemporaryDirectory()
        self.addCleanup(temporario.cleanup)
        self.db = str(Path(temporario.name) / "gerenciamento.db")
        schema = Path(__file__).resolve().parents[1] / "schema.sql"
        conexao = conectar(self.db)
        try:
            conexao.executescript(schema.read_text(encoding="utf-8"))
        finally:
            conexao.close()
        self.gerenciador = GerenciadorTarefa(RepositorioSQLite(self.db))
        self.vencimento = (date.today() + timedelta(days=5)).strftime("%d/%m/%Y")
        self.tarefa = criar_tarefa_simples(self.gerenciador, "Original", "Descrição",
                                          "Média", self.vencimento)

    def novo_gerenciador(self):
        return GerenciadorTarefa(RepositorioSQLite(self.db))

    def test_edicao_persiste_apos_nova_conexao(self):
        editar_simples(self.gerenciador, self.tarefa.id, " Cálculo ", " Álgebra ",
                       "Alta", self.vencimento)
        tarefa = self.novo_gerenciador().buscar_por_id(self.tarefa.id)
        self.assertEqual((tarefa.titulo, tarefa.descricao, tarefa.prioridade),
                         ("Cálculo", "Álgebra", Prioridade.ALTA))

    def test_edicao_concluida_nao_reabre(self):
        alternar_conclusao_simples(self.gerenciador, self.tarefa.id)
        editar_simples(self.gerenciador, self.tarefa.id, "Alterada", "Texto",
                       "Baixa", self.vencimento)
        tarefa = self.novo_gerenciador().buscar_por_id(self.tarefa.id)
        self.assertTrue(tarefa.concluida)
        self.assertEqual(tarefa.titulo, "Alterada")

    def test_concluir_e_reabrir_persistem(self):
        alternar_conclusao_simples(self.gerenciador, self.tarefa.id)
        self.assertTrue(self.novo_gerenciador().buscar_por_id(self.tarefa.id).concluida)
        alternar_conclusao_simples(self.gerenciador, self.tarefa.id)
        self.assertFalse(self.novo_gerenciador().buscar_por_id(self.tarefa.id).concluida)

    def test_excluir_persiste(self):
        excluir_simples(self.gerenciador, self.tarefa.id)
        self.assertEqual(self.novo_gerenciador().listar(), [])
        with self.assertRaises(ValueError):
            self.novo_gerenciador().buscar_por_id(self.tarefa.id)

    def test_titulo_invalido_nao_altera(self):
        with self.assertRaises(ValueError):
            editar_simples(self.gerenciador, self.tarefa.id, "   ", "Novo", "Alta", self.vencimento)
        self.assertEqual(self.novo_gerenciador().buscar_por_id(self.tarefa.id).titulo, "Original")

    def test_data_passada_alterada_e_rejeitada(self):
        ontem = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        with self.assertRaises(ValueError):
            editar_simples(self.gerenciador, self.tarefa.id, "Novo", "Novo", "Alta", ontem)
        self.assertEqual(self.novo_gerenciador().buscar_por_id(self.tarefa.id).titulo, "Original")

    def test_prioridade_invalida(self):
        with self.assertRaises(ValueError):
            editar_simples(self.gerenciador, self.tarefa.id, "Novo", "", "Crítica", self.vencimento)

    def test_operacao_em_checklist_bloqueada(self):
        checklist = TarefaChecklist(None, "Lista", "", Prioridade.BAIXA,
                                   date.today() + timedelta(days=5))
        self.gerenciador.criar(checklist)
        with self.assertRaises(TypeError):
            buscar_simples(self.gerenciador, checklist.id)
        with self.assertRaises(TypeError):
            excluir_simples(self.gerenciador, checklist.id)
        self.assertIsNotNone(self.novo_gerenciador().buscar_por_id(checklist.id))


if __name__ == "__main__":
    unittest.main()