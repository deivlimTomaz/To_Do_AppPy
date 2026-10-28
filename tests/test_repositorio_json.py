"""Demonstração de RepositorioJson sem unittest ou pytest.

Execute da raiz do projeto:
    python -m testes.test_repositorio_json
"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from package.repositorio_json import RepositorioJson


def secao(nome):
    print(f"\n{'=' * 60}\n{nome}\n{'=' * 60}")


def conferir(descricao, condicao):
    print(f"{'OK' if condicao else 'FALHA'} - {descricao}")


def main():
    # Um diretório temporário evita alterar dados reais do projeto.
    with TemporaryDirectory(prefix="teste_repositorio_json_") as pasta:
        caminho = Path(pasta) / "tarefas.json"

        secao("TESTE 1 - Criar repositório com caminho válido")
        repositorio = RepositorioJson(str(caminho))
        print("Repositório criado:", caminho.name)

        secao("TESTE 2 - Rejeitar caminho que não é string")
        try:
            RepositorioJson(123)
            print("FALHA - Caminho numérico foi aceito")
        except TypeError as erro:
            print("OK - TypeError esperado:", erro)

        secao("TESTE 3 - Rejeitar caminho em branco")
        try:
            RepositorioJson("   ")
            print("FALHA - Caminho vazio foi aceito")
        except ValueError as erro:
            print("OK - ValueError esperado:", erro)

        secao("TESTE 4 - Salvar dicionário com lista e acentos")
        dados = {
            "lista": "Estudos",
            "tarefas": [
                {"id": 1, "titulo": "Estudar Python", "prioridade": "ALTA", "concluida": False},
                {"id": 2, "titulo": "Revisar orientação a objetos", "prioridade": "MEDIA", "concluida": True},
            ],
        }
        repositorio.salvar(dados)
        conferir("Arquivo JSON criado", caminho.is_file())
        print("Conteúdo salvo no arquivo:")
        print(caminho.read_text(encoding="utf-8"))

        secao("TESTE 5 - Carregar e comparar dados")
        carregados = repositorio.carregar()
        conferir("Dados carregados são iguais aos originais", carregados == dados)
        print("Tarefas recuperadas:", len(carregados["tarefas"]))

        secao("TESTE 6 - Sobrescrever arquivo existente")
        novos_dados = {"lista": "Trabalho", "tarefas": [{"id": 3, "titulo": "Preparar relatório"}]}
        repositorio.salvar(novos_dados)
        conferir("Arquivo contém os novos dados", repositorio.carregar() == novos_dados)
        conferir("Dados antigos foram substituídos", repositorio.carregar() != dados)

        secao("TESTE 7 - Salvar e carregar lista vazia")
        repositorio.salvar([])
        conferir("Lista vazia recuperada", repositorio.carregar() == [])

        secao("TESTE 8 - Arquivo inexistente")
        inexistente = RepositorioJson(str(Path(pasta) / "nao_existe.json"))
        try:
            inexistente.carregar()
            print("FALHA - Arquivo inexistente foi carregado")
        except FileNotFoundError as erro:
            print("OK - FileNotFoundError esperado:", erro.filename)

        secao("TESTE 9 - Arquivo com JSON inválido")
        caminho.write_text("{isto não é um JSON válido", encoding="utf-8")
        try:
            repositorio.carregar()
            print("FALHA - JSON inválido foi aceito")
        except json.JSONDecodeError as erro:
            print(f"OK - JSONDecodeError esperado (linha {erro.lineno}, coluna {erro.colno})")

        secao("TESTE 10 - Dados não serializáveis")
        try:
            repositorio.salvar({"valores": {1, 2, 3}})  # set não é serializável em JSON
            print("FALHA - set foi serializado sem conversão")
        except TypeError as erro:
            print("OK - TypeError esperado:", erro)

        secao("FIM DA DEMONSTRAÇÃO")
        print("Os arquivos temporários serão removidos automaticamente.")
        print("Observação: OK significa que o comportamento esperado ocorreu.")


if __name__ == "__main__":
    main()

