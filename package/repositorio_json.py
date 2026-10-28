from package.repositorio import Repositorio
import json

class RepositorioJson(Repositorio):

    def __init__(self, caminho_arq: str):
        
        if not isinstance(caminho_arq, str):
            raise TypeError("Caminho inserido inválido!")
        if not caminho_arq.strip():
            raise ValueError("Erro: caminho inserido em branco!")
        
        self._caminho_arq = caminho_arq

    def salvar(self, dados):
        
        with open(self._caminho_arq, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def carregar(self):

        with open(self._caminho_arq, "r", encoding="utf-8") as arquivo:
            dados_carregados = json.load(arquivo)
        return dados_carregados
