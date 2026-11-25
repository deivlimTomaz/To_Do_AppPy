import tempfile
import unittest

from datetime import date, timedelta
from pathlib import Path

from interface.recorrencia_operacoes import (
    criar_recorrente,
    editar_recorrente,
    alternar_conclusao,
    gerar_proxima,
    excluir_recorrente,
    buscar_recorrente,
)

from package.conexao import conectar
from package.gerenciador_tarefa import GerenciadorTarefa
from package.repositorio_sqlite import RepositorioSQLite
from package.tarefa_simples import TarefaSimples
from package.prioridade import Prioridade


class TestInterfaceRecorrencia(unittest.TestCase):

    def setUp(self):

        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)

        self.caminho = str(
            Path(pasta.name) / "teste.db"
        )

        conexao = conectar(self.caminho)

        schema = (
            Path(__file__).resolve().parents[1]
            / "schema.sql"
        )

        try:
            conexao.executescript(
                schema.read_text(encoding="utf-8")
            )

        finally:
            conexao.close()

        self.gerenciador = GerenciadorTarefa(
            RepositorioSQLite(self.caminho)
        )

        self.data = (
            date.today() + timedelta(days=2)
        ).strftime("%d/%m/%Y")

    def criar(self):

        return criar_recorrente(
            self.gerenciador,
            "Revisar",
            "POO",
            "Alta",
            self.data,
            "Semanal",
            "2"
        )

    def test_criar_e_persistir(self):

        tarefa = buscar_recorrente(
            self.gerenciador,
            self.criar().id
        )

        self.assertEqual(
            (
                tarefa.recorrencia.frequencia,
                tarefa.recorrencia.intervalo
            ),
            ("semanal", 2)
        )

    def test_editar_frequencia_intervalo_e_dados(self):

        tarefa = self.criar()

        editar_recorrente(
            self.gerenciador,
            tarefa.id,
            "Revisão",
            "Algebra",
            "Baixa",
            self.data,
            "Mensal",
            "3"
        )

        atual = buscar_recorrente(
            self.gerenciador,
            tarefa.id
        )

        self.assertEqual(
            (
                atual.titulo,
                atual.recorrencia.frequencia,
                atual.recorrencia.intervalo
            ),
            ("Revisão", "mensal", 3)
        )

    def test_editar_concluida_preserva_estado(self):

        tarefa = self.criar()

        alternar_conclusao(
            self.gerenciador,
            tarefa.id
        )

        editar_recorrente(
            self.gerenciador,
            tarefa.id,
            "Novo",
            "",
            "Média",
            self.data,
            "Diária",
            "1"
        )

        self.assertTrue(
            buscar_recorrente(
                self.gerenciador,
                tarefa.id
            ).concluida
        )

    def test_gerar_exige_conclusao(self):

        tarefa = self.criar()

        with self.assertRaises(ValueError):
            gerar_proxima(
                self.gerenciador,
                tarefa.id
            )

    def test_geracao_usa_frequencia_editada(self):

        tarefa = self.criar()

        editar_recorrente(
            self.gerenciador,
            tarefa.id,
            "Revisar",
            "",
            "Alta",
            self.data,
            "Diária",
            "3"
        )

        alternar_conclusao(
            self.gerenciador,
            tarefa.id
        )

        proxima = gerar_proxima(
            self.gerenciador,
            tarefa.id
        )

        self.assertNotEqual(
            proxima.id,
            tarefa.id
        )

        self.assertEqual(
            proxima.data_vencimento,
            date.today() + timedelta(days=5)
        )

        self.assertFalse(proxima.concluida)

        self.assertEqual(
            proxima.recorrencia.intervalo,
            3
        )

    def test_reabrir(self):

        tarefa = self.criar()

        alternar_conclusao(
            self.gerenciador,
            tarefa.id
        )

        alternar_conclusao(
            self.gerenciador,
            tarefa.id
        )

        self.assertFalse(
            buscar_recorrente(
                self.gerenciador,
                tarefa.id
            ).concluida
        )

    def test_excluir(self):

        tarefa = self.criar()

        excluir_recorrente(
            self.gerenciador,
            tarefa.id
        )

        with self.assertRaises(ValueError):
            buscar_recorrente(
                self.gerenciador,
                tarefa.id
            )

    def test_intervalo_invalido(self):

        for intervalo in (
            "0",
            "-1",
            "1.5",
            "abc",
            ""
        ):

            with self.subTest(intervalo=intervalo):

                with self.assertRaises(ValueError):
                    criar_recorrente(
                        self.gerenciador,
                        "Revisar",
                        "",
                        "Alta",
                        self.data,
                        "Semanal",
                        intervalo
                    )

    def test_tipo_invalido(self):

        simples = self.gerenciador.criar(
            TarefaSimples(
                None,
                "Simples",
                "",
                Prioridade.MEDIA,
                date.today()
            )
        )

        with self.assertRaises(TypeError):

            editar_recorrente(
                self.gerenciador,
                simples.id,
                "Mudada",
                "",
                "Baixa",
                self.data,
                "Diária",
                "1"
            )

    def test_edicao_invalida_nao_modifica_configuracao(self):

        tarefa = self.criar()

        with self.assertRaises(ValueError):

            editar_recorrente(
                self.gerenciador,
                tarefa.id,
                "Novo",
                "",
                "Alta",
                self.data,
                "Mensal",
                "0"
            )

        atual = buscar_recorrente(
            self.gerenciador,
            tarefa.id
        )

        self.assertEqual(
            (
                atual.titulo,
                atual.recorrencia.frequencia
            ),
            ("Revisar", "semanal")
        )


if __name__ == "__main__":
    unittest.main()