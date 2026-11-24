"""Janela para gerenciar checklists existentes."""

from tkinter import messagebox

import customtkinter as ctk

from interface.checklist_formulario import excluir_checklist

from interface.janela_formulario_checklist import (
    JanelaFormularioChecklist
)

from interface.checklist_operacoes import (
    buscar_checklist,
    adicionar_item,
    remover_item,
    alternar_item,
    alternar_conclusao
)


class JanelaChecklist(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        gerenciador,
        id_tarefa,
        ao_alterar
    ):
        super().__init__(parent)

        self.gerenciador = gerenciador
        self.id_tarefa = id_tarefa
        self.ao_alterar = ao_alterar

        self.janela_edicao = None

        self.title("Gerenciar checklist")
        self.geometry("560x620")
        self.minsize(480, 500)

        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Título

        self.titulo = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        self.titulo.grid(
            row=0,
            column=0,
            padx=22,
            pady=(20, 4),
            sticky="w"
        )

        # Estado

        self.estado = ctk.CTkLabel(
            self,
            text=""
        )

        self.estado.grid(
            row=1,
            column=0,
            padx=22,
            sticky="w"
        )

        # Formulário de novos itens

        entrada = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        entrada.grid(
            row=2,
            column=0,
            padx=22,
            pady=15,
            sticky="ew"
        )

        entrada.grid_columnconfigure(
            0,
            weight=1
        )

        self.campo_item = ctk.CTkEntry(
            entrada,
            placeholder_text="Novo item"
        )

        self.campo_item.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )

        self.botao_adicionar = ctk.CTkButton(
            entrada,
            text="Adicionar",
            width=100,
            command=self.adicionar
        )

        self.botao_adicionar.grid(
            row=0,
            column=1
        )

        # Listagem

        self.lista_itens = ctk.CTkScrollableFrame(
            self
        )

        self.lista_itens.grid(
            row=3,
            column=0,
            padx=22,
            pady=(0, 12),
            sticky="nsew"
        )

        self.lista_itens.grid_columnconfigure(
            1,
            weight=1
        )

        # Rodapé

        rodape = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        rodape.grid(
            row=4,
            column=0,
            padx=22,
            pady=(0, 22),
            sticky="ew"
        )

        rodape.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        # Concluir ou reabrir

        self.botao_estado = ctk.CTkButton(
            rodape,
            text="",
            command=self.alternar_estado
        )

        self.botao_estado.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 6)
        )

        # Fechar

        ctk.CTkButton(
            rodape,
            text="Fechar",
            fg_color="transparent",
            border_width=1,
            text_color=("black", "white"),
            command=self.destroy
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(6, 0)
        )

        # Editar dados gerais

        ctk.CTkButton(
            rodape,
            text="Editar dados",
            command=self.editar_dados
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 6),
            pady=(10, 0)
        )

        # Excluir checklist

        ctk.CTkButton(
            rodape,
            text="Excluir checklist",
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.excluir
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(6, 0),
            pady=(10, 0)
        )

        self.carregar()

    def executar_operacao(self, operacao):

        try:
            operacao()

        except (ValueError, TypeError, IndexError) as erro:

            messagebox.showwarning(
                "Operação não permitida",
                str(erro),
                parent=self
            )

            return False

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self
            )

            return False

        self.carregar()
        self.ao_alterar()

        return True

    def carregar(self):

        tarefa = buscar_checklist(
            self.gerenciador,
            self.id_tarefa
        )

        feitos, total = tarefa.progresso()

        self.titulo.configure(
            text=tarefa.titulo
        )

        situacao = (
            "Concluído"
            if tarefa.concluida
            else "Pendente"
        )

        self.estado.configure(
            text=(
                f"{situacao} | "
                f"{feitos}/{total} itens marcados"
            )
        )

        self.botao_estado.configure(
            text=(
                "Reabrir checklist"
                if tarefa.concluida
                else "Concluir checklist"
            )
        )

        estado_controles = (
            "disabled"
            if tarefa.concluida
            else "normal"
        )

        self.campo_item.configure(
            state=estado_controles
        )

        self.botao_adicionar.configure(
            state=estado_controles
        )

        # Remove a representação visual anterior

        for widget in self.lista_itens.winfo_children():
            widget.destroy()

        if not tarefa.itens:

            ctk.CTkLabel(
                self.lista_itens,
                text="Nenhum item adicionado."
            ).grid(
                row=0,
                column=0,
                pady=20
            )

        # Reconstrói os itens

        for indice, item in enumerate(tarefa.itens):

            variavel = ctk.BooleanVar(
                value=item.feito
            )

            checkbox = ctk.CTkCheckBox(
                self.lista_itens,
                text=item.texto,
                variable=variavel,
                state=estado_controles,
                command=lambda i=indice: self.marcar(i)
            )

            checkbox.grid(
                row=indice,
                column=0,
                columnspan=2,
                sticky="w",
                padx=8,
                pady=8
            )

            botao = ctk.CTkButton(
                self.lista_itens,
                text="Remover",
                width=82,
                state=estado_controles,
                command=lambda i=indice: self.remover(i)
            )

            botao.grid(
                row=indice,
                column=2,
                padx=8,
                pady=8
            )

    def adicionar(self):

        texto = self.campo_item.get()

        if self.executar_operacao(
            lambda: adicionar_item(
                self.gerenciador,
                self.id_tarefa,
                texto
            )
        ):
            self.campo_item.delete(
                0,
                "end"
            )

    def marcar(self, indice):

        self.executar_operacao(
            lambda: alternar_item(
                self.gerenciador,
                self.id_tarefa,
                indice
            )
        )

    def remover(self, indice):

        confirmou = messagebox.askyesno(
            "Remover item",
            "Deseja remover este item?",
            parent=self
        )

        if confirmou:

            self.executar_operacao(
                lambda: remover_item(
                    self.gerenciador,
                    self.id_tarefa,
                    indice
                )
            )

    def alternar_estado(self):

        self.executar_operacao(
            lambda: alternar_conclusao(
                self.gerenciador,
                self.id_tarefa
            )
        )

    def editar_dados(self):

        if (
            self.janela_edicao is not None
            and self.janela_edicao.winfo_exists()
        ):
            self.janela_edicao.focus()
            return

        # Libera a janela atual para abrir o formulário modal.

        self.grab_release()

        self.janela_edicao = JanelaFormularioChecklist(
            self,
            self.gerenciador,
            self.ao_editar_dados,
            self.id_tarefa
        )

        self.janela_edicao.bind(
            "<Destroy>",
            self._retomar_foco
        )

    def _retomar_foco(self, evento):

        if (
            evento.widget is self.janela_edicao
            and self.winfo_exists()
        ):
            self.grab_set()

    def ao_editar_dados(self, tarefa):

        self.carregar()
        self.ao_alterar()

    def excluir(self):

        confirmou = messagebox.askyesno(
            "Excluir checklist",
            (
                "Excluir o checklist e todos "
                "os seus itens permanentemente?"
            ),
            parent=self
        )

        if not confirmou:
            return

        try:

            excluir_checklist(
                self.gerenciador,
                self.id_tarefa
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao excluir",
                str(erro),
                parent=self
            )

            return

        self.destroy()
        self.ao_alterar()