class ItemChecklist:

    def __init__(self, texto: str):
        
        self._feito = False
        self._texto = texto


    def marcar(self):

        self._feito = True

    def desmarcar(self):

        self._feito = False

    @property
    def texto(self) -> str:

        return self._texto

    @property
    def feito(self) -> bool:

        return self._feito

    # Serialização dos objetos de item_checklist
    def para_dict(self):
        dados_item_check = {
            "texto": self._texto,
            "feito": self._feito
        }

        return dados_item_check


    def __str__(self) -> str:

        status = "[X]" if self._feito else "[ ]"

        return f"{status} - {self._texto}"
