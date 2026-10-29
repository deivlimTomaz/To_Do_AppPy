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

    # Desserialização
    @classmethod
    def de_dict(cls, dados_item_check: dict):

        # Recuperação de dados dos itens
        extract_texto = dados_item_check["texto"]
        extract_feito = dados_item_check["feito"]

        dados_chlst_recuperados = cls(extract_texto)

        if extract_feito == True:
            dados_chlst_recuperados.marcar()

        return dados_chlst_recuperados
