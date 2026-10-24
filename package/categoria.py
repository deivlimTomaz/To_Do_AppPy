class Categoria:

    def __init__(self, cor: str, tipo: str):
        if not isinstance(cor, str) or not cor.strip():
            raise TypeError("A cor deve ser em texto")

        if not isinstance(tipo, str) or not tipo.strip():
            raise TypeError("O tipo deve ser em texto")

        self._cor = cor
        self._tipo = tipo


    @property
    def cor(self) -> str:
        return self._cor

    @property
    def tipo(self) -> str:
        return self._tipo


