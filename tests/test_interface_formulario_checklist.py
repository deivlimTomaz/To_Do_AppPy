import tempfile
import unittest

from datetime import date, timedelta
from pathlib import Path

from interface.checklist_formulario import (
    criar_checklist,
    editar_checklist,
    excluir_checklist
)

from interface.checklist_operacoes import (
    adicionar_item,
    alternar_item,
    alternar_conclusao
)

from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_simples import TarefaSimples
from package.prioridade import Prioridade


class TestFormularioChecklist(unittest.TestCase):

    def setUp(self):

        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)

        caminho = Path(pasta.name) / "checklist.db"

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

        self.data = (
            date.today() + timedelta(days=3)
        ).strftime("%d/%m/%Y")

    def criar(self):

        return criar_checklist(
            self.gerenciador,
            "Compras",
            "Mercado",
            "Média",
            self.data
        )

    def test_criar_checklist_vazio_persistido(self):

        tarefa = self.criar()

        recuperada = self.gerenciador.buscar_por_id(
            tarefa.id
        )

        self.assertEqual(
            recuperada.titulo,
            "Compras"
        )

        self.assertEqual(
            recuperada.itens,
            []
        )

    def test_editar_dados_preservando_itens(self):

        tarefa = self.criar()

        adicionar_item(
            self.gerenciador,
            tarefa.id,
            "Leite"
        )

        editar_checklist(
            self.gerenciador,
            tarefa.id,
            "Compras novas",
            "Padaria",
            "Alta",
            self.data
        )

        recuperada = self.gerenciador.buscar_por_id(
            tarefa.id
        )

        self.assertEqual(
            recuperada.titulo,
            "Compras novas"
        )

        self.assertEqual(
            recuperada.prioridade,
            Prioridade.ALTA
        )

        self.assertEqual(
            recuperada.itens[0].texto,
            "Leite"
        )

    def test_editar_concluido_mantem_conclusao(self):

        tarefa = self.criar()

        adicionar_item(
            self.gerenciador,
            tarefa.id,
            "Leite"
        )

        alternar_item(
            self.gerenciador,
            tarefa.id,
            0
        )

        alternar_conclusao(
            self.gerenciador,
            tarefa.id
        )

        editar_checklist(
            self.gerenciador,
            tarefa.id,
            "Compras completas",
            "",
            "Baixa",
            self.data
        )

        recuperada = self.gerenciador.buscar_por_id(
            tarefa.id
        )

        self.assertTrue(
            recuperada.concluida
        )

        self.assertTrue(
            recuperada.itens[0].feito
        )

    def test_exclusao_com_itens(self):

        tarefa = self.criar()

        adicionar_item(
            self.gerenciador,
            tarefa.id,
            "Leite"
        )

        excluir_checklist(
            self.gerenciador,
            tarefa.id
        )

        with self.assertRaises(ValueError):

            self.gerenciador.buscar_por_id(
                tarefa.id
            )

    def test_titulo_vazio(self):

        with self.assertRaises(ValueError):

            criar_checklist(
                self.gerenciador,
                "   ",
                "",
                "Média",
                self.data
            )

    def test_prioridade_invalida(self):

        with self.assertRaises(ValueError):

            criar_checklist(
                self.gerenciador,
                "Compras",
                "",
                "Urgentíssima",
                self.data
            )

    def test_data_invalida(self):

        with self.assertRaises(ValueError):

            criar_checklist(
                self.gerenciador,
                "Compras",
                "",
                "Média",
                "31/02/2026"
            )

    def test_data_passada_no_cadastro(self):

        with self.assertRaises(ValueError):

            criar_checklist(
                self.gerenciador,
                "Compras",
                "",
                "Média",
                "01/01/2000"
            )

    def test_bloqueia_tipo_simples(self):

        simples = self.gerenciador.criar(
            TarefaSimples(
                None,
                "Simples",
                "",
                Prioridade.BAIXA,
                date.today() + timedelta(days=1)
            )
        )

        with self.assertRaises(TypeError):

            editar_checklist(
                self.gerenciador,
                simples.id,
                "Outro",
                "",
                "Baixa",
                self.data
            )

        with self.assertRaises(TypeError):

            excluir_checklist(
                self.gerenciador,
                simples.id
            )


if __name__ == "__main__":
    unittest.main()