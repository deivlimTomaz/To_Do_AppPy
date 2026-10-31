from package.gerenciador_tarefa import GerenciadorTarefa
from package.repositorio import Repositorio

class Menu:
    def __init__(self, gerenciador: GerenciadorTarefa, repositorio: Repositorio):
        self._gerenciador = gerenciador
        self._repositorio = repositorio

    def mostrar_menu(self):
        print("\n========= APP TO-DO ==========\n")
        print("1. Listar tarefa")
        print("2. Criar tarefa")
        print("3. Editar tarefa")
        print("4. Concluir tarefa")
        print("5. Excluir tarefa")
        print("6. Salvar alterações")
        print("7. Sair do aplicativo")
        print("=" * 20)
