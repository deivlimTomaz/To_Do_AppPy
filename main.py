from package.menu import Menu
from package.lista import Lista
from package.categoria import Categoria
from package.gerenciador_tarefa import GerenciadorTarefa
from package.repositorio_json import RepositorioJson

if __name__ == "__main__":

    categoria = Categoria("Azul", "Estudos")

    lista = Lista("Minhas tarefas", categoria)

    gerenciador = GerenciadorTarefa(lista)

    repositorio = RepositorioJson("tarefas.json")

    sistema = Menu(gerenciador, repositorio)

    sistema.mostrar_menu()
