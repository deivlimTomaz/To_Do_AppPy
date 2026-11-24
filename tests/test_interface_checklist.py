import tempfile
import unittest

from datetime import date, timedelta
from pathlib import Path

from interface.checklist_operacoes import (
    buscar_checklist,
    adicionar_item,
    remover_item,
    alternar_item,
    alternar_conclusao,
)

from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.prioridade import Prioridade
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_simples import TarefaSimples


class TestInterfaceChecklist(unittest.TestCase):

    def setUp(self):

        diretorio = tempfile.TemporaryDirectory()
        self.addCleanup(diretorio.cleanup)

        caminho = Path(diretorio.name) / "teste.db"

        schema = (
            Path(__file__).resolve().parents[1]
            / "schema.sql"
        )

        conexao = conectar(str(caminho))

        try:
            conexao.executescript(
                schema.read_text(encoding="utf-8")
            )
        finally:
            conexao.close()

        self.gerenciador = GerenciadorTarefa(
            RepositorioSQLite(str(caminho))
        )

        self.tarefa = self.gerenciador.criar(
            TarefaChecklist(
                None,
                "Compras",
                "",
                Prioridade.MEDIA,
                date.today() + timedelta(days=3)
            )
        )

    def buscar(self):
        return buscar_checklist(
            self.gerenciador,
            self.tarefa.id
        )

    def test_adicionar_e_persistir(self):

        adicionar_item(
            self.gerenciador,
            self.tarefa.id,
            "Leite"
        )

        self.assertEqual(
            self.buscar().itens[0].texto,
            "Leite"
        )

    def test_marcar_e_desmarcar(self):

        adicionar_item(
            self.gerenciador,
            self.tarefa.id,
            "Leite"
        )

        alternar_item(
            self.gerenciador,
            self.tarefa.id,
            0
        )

        self.assertTrue(
            self.buscar().itens[0].feito
        )

        alternar_item(
            self.gerenciador,
            self.tarefa.id,
            0
        )

        self.assertFalse(
            self.buscar().itens[0].feito
        )

    def test_remover(self):

        adicionar_item(
            self.gerenciador,
            self.tarefa.id,
            "Leite"
        )

        remover_item(
            self.gerenciador,
            self.tarefa.id,
            0
        )

        self.assertEqual(
            self.buscar().itens,
            []
        )

    def test_conclusao_exige_itens_marcados(self):

        # Checklist vazio não pode ser concluído
        with self.assertRaises(ValueError):
            alternar_conclusao(
                self.gerenciador,
                self.tarefa.id
            )

        adicionar_item(
            self.gerenciador,
            self.tarefa.id,
            "Leite"
        )

        # Item pendente impede conclusão
        with self.assertRaises(ValueError):
            alternar_conclusao(
                self.gerenciador,
                self.tarefa.id
            )

        alternar_item(
            self.gerenciador,
            self.tarefa.id,
            0
        )

        alternar_conclusao(
            self.gerenciador,
            self.tarefa.id
        )

        self.assertTrue(
            self.buscar().concluida
        )

    def test_concluido_bloqueia_itens_e_reabrir_libera(self):

        adicionar_item(
            self.gerenciador,
            self.tarefa.id,
            "Leite"
        )

        alternar_item(
            self.gerenciador,
            self.tarefa.id,
            0
        )

        alternar_conclusao(
            self.gerenciador,
            self.tarefa.id
        )

        with self.assertRaises(ValueError):
            adicionar_item(
                self.gerenciador,
                self.tarefa.id,
                "Pão"
            )

        with self.assertRaises(ValueError):
            alternar_item(
                self.gerenciador,
                self.tarefa.id,
                0
            )

        with self.assertRaises(ValueError):
            remover_item(
                self.gerenciador,
                self.tarefa.id,
                0
            )

        # Reabre o checklist
        alternar_conclusao(
            self.gerenciador,
            self.tarefa.id
        )

        self.assertFalse(
            self.buscar().concluida
        )

        adicionar_item(
            self.gerenciador,
            self.tarefa.id,
            "Pão"
        )

        self.assertEqual(
            len(self.buscar().itens),
            2
        )

    def test_rejeitar_item_vazio(self):

        with self.assertRaises(ValueError):
            adicionar_item(
                self.gerenciador,
                self.tarefa.id,
                "   "
            )

        self.assertEqual(
            self.buscar().itens,
            []
        )

    def test_rejeitar_tipo_incorreto(self):

        simples = self.gerenciador.criar(
            TarefaSimples(
                None,
                "Simples",
                "",
                Prioridade.BAIXA,
                date.today() + timedelta(days=2)
            )
        )

        with self.assertRaises(TypeError):
            buscar_checklist(
                self.gerenciador,
                simples.id
            )


if __name__ == "__main__":
    unittest.main()