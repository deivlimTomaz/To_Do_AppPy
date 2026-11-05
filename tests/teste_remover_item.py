"""
Testes do tópico 4 — TarefaChecklist.remover_item(indice).

Estrutura esperada (pasta de testes SEPARADA da pasta package):

    <raiz_do_projeto>/
    ├── package/              <- pacote com tarefa, item_checklist, prioridade
    ├── tarefa_checklist.py   <- a classe que estamos testando (fora do pacote)
    └── testes/               <- sua pasta de testes (onde está este arquivo)
        └── teste_remover_item.py

Como rodar (funciona dos dois jeitos):

    # 1) de dentro da PASTA-RAIZ do projeto:
    python -m unittest testes.teste_remover_item -v

    # 2) de DENTRO da pasta de testes:
    python teste_remover_item.py

Se o seu 'tarefa_checklist.py' ficar DENTRO da pasta 'package', troque o
import de TarefaChecklist abaixo pela linha comentada
(from package.tarefa_checklist import TarefaChecklist).
"""
import sys
import unittest
from datetime import date
from pathlib import Path

# --- faz o teste encontrar 'package' e 'tarefa_checklist' mesmo com as -------
# --- pastas separadas. A raiz do projeto é descoberta a partir da ---------
# --- localização DESTE arquivo: como ele está em <raiz>/testes/, ----------
# --- o "pai do pai" (<raiz>) é a pasta que precisa entrar no caminho. -----
RAIZ_DO_PROJETO = Path(__file__).resolve().parent.parent
if str(RAIZ_DO_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_DO_PROJETO))

try:  # caso: tarefa_checklist.py está FORA do package (na raiz do projeto)
    from tarefa_checklist import TarefaChecklist
except ImportError:  # caso: tarefa_checklist.py está DENTRO do package
    from package.tarefa_checklist import TarefaChecklist

from package.prioridade import Prioridade


class TesteRemoverItem(unittest.TestCase):
    """Casos de uso do método remover_item(indice)."""

    def setUp(self):
        """Tarefa de exemplo com três itens:
        [Ler capítulo, Fazer resumo, Resolver exercícios]."""
        self.tarefa = TarefaChecklist(
            1, "Estudar", "Revisar capítulo 1", Prioridade.ALTA, date(2026, 11, 10)
        )
        self.tarefa.adicionar_item("Ler capítulo")
        self.tarefa.adicionar_item("Fazer resumo")
        self.tarefa.adicionar_item("Resolver exercícios")

    def test_remover_item_reduz_a_lista(self):
        """Remover o item do meio: sobram os outros dois, na ordem."""
        antes = list(self.tarefa.itens)       # [Ler, Resumo, Exercícios]

        self.tarefa.remover_item(1)

        depois = list(self.tarefa.itens)
        self.assertEqual(len(depois), 2)
        # conferimos por IDENTIDADE (não depende de como o item guarda o texto):
        self.assertIs(depois[0], antes[0])    # "Ler capítulo" segue primeiro
        self.assertIs(depois[1], antes[2])    # "Exercícios" subiu uma posição

    def test_remover_o_primeiro_item(self):
        """Remover o índice 0 tira o primeiro item e desloca os demais."""
        antes = list(self.tarefa.itens)

        self.tarefa.remover_item(0)

        depois = list(self.tarefa.itens)
        self.assertEqual(len(depois), 2)
        self.assertIs(depois[0], antes[1])    # "Fazer resumo" virou o primeiro
        self.assertIs(depois[1], antes[2])

    def test_remover_o_ultimo_item(self):
        """Remover o último índice válido (len - 1) tira o último item."""
        antes = list(self.tarefa.itens)

        self.tarefa.remover_item(2)

        depois = list(self.tarefa.itens)
        self.assertEqual(len(depois), 2)
        self.assertIs(depois[0], antes[0])    # os dois primeiros seguem intactos
        self.assertIs(depois[1], antes[1])

    def test_remover_item_desloca_os_indices_seguintes(self):
        """Depois de remover, o item seguinte assume o índice do removido:
        os índices NOVOS é que valem."""
        self.tarefa.remover_item(0)   # sai "Ler capítulo"; "Fazer resumo" passa a ser índice 0
        self.tarefa.marcar_item(0)    # marca "Fazer resumo"

        self.assertTrue(self.tarefa.itens[0].feito)
        self.assertFalse(self.tarefa.itens[1].feito)
        self.assertEqual(self.tarefa.progresso(), (1, 2))

    def test_remover_item_atualiza_o_progresso(self):
        """Progresso recalculado corretamente ao remover item FEITO e item PENDENTE."""
        self.tarefa.marcar_item(0)                  # 1 feito de 3
        self.assertEqual(self.tarefa.progresso(), (1, 3))

        self.tarefa.remover_item(0)                 # removeu o item que estava feito -> 0 de 2
        self.assertEqual(self.tarefa.progresso(), (0, 2))

        self.tarefa.marcar_item(0)                  # marca o novo primeiro -> 1 de 2
        self.tarefa.remover_item(1)                 # remove um item pendente -> 1 de 1
        self.assertEqual(self.tarefa.progresso(), (1, 1))

    def test_remover_item_de_tarefa_concluida_da_valor_error(self):
        """Tarefa concluída bloqueia remoção (mesma regra dos outros métodos)."""
        self.tarefa.marcar_item(0)
        self.tarefa.marcar_item(1)
        self.tarefa.marcar_item(2)
        self.tarefa.concluir()

        with self.assertRaises(ValueError):
            self.tarefa.remover_item(0)

    def test_remover_item_com_indice_nao_inteiro(self):
        """Índice que não é int dá TypeError (passa pela _validar_indice)."""
        for indice in (0.0, "1", None, []):
            with self.subTest(indice=indice):
                with self.assertRaises(TypeError):
                    self.tarefa.remover_item(indice)

    def test_remover_item_fora_do_intervalo(self):
        """Índice igual ao tamanho, muito grande ou negativo dão IndexError."""
        for indice in (3, 99, -1):
            with self.subTest(indice=indice):
                with self.assertRaises(IndexError):
                    self.tarefa.remover_item(indice)

    def test_remover_item_de_lista_vazia(self):
        """Sem nenhum item, qualquer índice é inválido -> IndexError."""
        tarefa_vazia = TarefaChecklist(
            2, "Lista vazia", "Sem itens", Prioridade.BAIXA, date(2026, 11, 11)
        )
        with self.assertRaises(IndexError):
            tarefa_vazia.remover_item(0)

    def test_remover_todos_os_itens_esvazia_a_tarefa(self):
        """Dá para remover item por item até esvaziar (progresso 0/0)... e a
        lista vazia faz concluir() recusar (todos_feitos() é False)."""
        self.tarefa.remover_item(0)
        self.tarefa.remover_item(0)
        self.tarefa.remover_item(0)

        self.assertEqual(self.tarefa.itens, [])
        self.assertEqual(self.tarefa.progresso(), (0, 0))

        with self.assertRaises(ValueError):
            self.tarefa.concluir()


if __name__ == "__main__":
    unittest.main(verbosity=2)
