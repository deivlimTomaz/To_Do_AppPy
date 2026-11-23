"""Teste do cadastro pela camada de formulário, sem abrir janelas."""
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from interface.cadastro import criar_tarefa_simples
from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.prioridade import Prioridade
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_simples import TarefaSimples


class TestInterfaceCadastro(unittest.TestCase):
    def setUp(self):
        temporario = tempfile.TemporaryDirectory()
        self.addCleanup(temporario.cleanup)
        caminho = Path(temporario.name) / "cadastro.db"
        schema = Path(__file__).resolve().parents[1] / "schema.sql"
        conexao = conectar(str(caminho))
        try:
            conexao.executescript(schema.read_text(encoding="utf-8"))
        finally:
            conexao.close()
        self.gerenciador = GerenciadorTarefa(RepositorioSQLite(str(caminho)))
        self.data = (date.today() + timedelta(days=3)).strftime("%d/%m/%Y")

    def test_cadastrar_e_persistir_tarefa(self):
        tarefa = criar_tarefa_simples(self.gerenciador, " Estudar Python ",
                                      " Exercícios ", "Alta", self.data)
        self.assertIsInstance(tarefa, TarefaSimples)
        self.assertIsInstance(tarefa.id, int)
        recuperada = self.gerenciador.buscar_por_id(tarefa.id)
        self.assertEqual(recuperada.titulo, "Estudar Python")
        self.assertEqual(recuperada.descricao, "Exercícios")
        self.assertEqual(recuperada.prioridade, Prioridade.ALTA)
        self.assertEqual(recuperada.data_vencimento.strftime("%d/%m/%Y"), self.data)
        self.assertFalse(recuperada.concluida)

    def test_titulo_vazio_nao_persiste(self):
        with self.assertRaises(ValueError):
            criar_tarefa_simples(self.gerenciador, "   ", "", "Média", self.data)
        self.assertEqual(self.gerenciador.listar(), [])

    def test_data_invalida_nao_persiste(self):
        with self.assertRaises(ValueError):
            criar_tarefa_simples(self.gerenciador, "Tarefa", "", "Média", "31/02/2027")
        self.assertEqual(self.gerenciador.listar(), [])

    def test_data_passada_nao_persiste(self):
        ontem = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        with self.assertRaises(ValueError):
            criar_tarefa_simples(self.gerenciador, "Tarefa", "", "Média", ontem)
        self.assertEqual(self.gerenciador.listar(), [])

    def test_prioridade_invalida_nao_persiste(self):
        with self.assertRaises(ValueError):
            criar_tarefa_simples(self.gerenciador, "Tarefa", "", "Urgente", self.data)
        self.assertEqual(self.gerenciador.listar(), [])

    def test_tres_prioridades(self):
        for nome, enum in [("Baixa", Prioridade.BAIXA), ("Média", Prioridade.MEDIA), ("Alta", Prioridade.ALTA)]:
            tarefa = criar_tarefa_simples(self.gerenciador, nome, "", nome, self.data)
            self.assertEqual(tarefa.prioridade, enum)
        self.assertEqual(len(self.gerenciador.listar()), 3)


if __name__ == "__main__":
    unittest.main()
