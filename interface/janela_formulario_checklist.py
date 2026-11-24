"""Formulário para criar e editar dados gerais de checklists."""

from datetime import date
from tkinter import messagebox

import customtkinter as ctk

from interface.checklist_formulario import (
    criar_checklist,
    editar_checklist
)

from interface.checklist_operacoes import buscar_checklist


class JanelaFormularioChecklist(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        gerenciador,
        ao_salvar,
        id_tarefa=None
    ):
        super().__init__(parent)

        self.gerenciador = gerenciador
        self.ao_salvar = ao_salvar
        self.id_tarefa = id_tarefa

        self.title(
            "Editar checklist"
            if id_tarefa is not None
            else "Novo checklist"
        )

        self.geometry("490x520")
        self.minsize(450, 500)

        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        corpo = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        corpo.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=28,
            pady=22
        )

        corpo.grid_columnconfigure(0, weight=1)

        # Título do formulário

        ctk.CTkLabel(
            corpo,
            text=self.title(),
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 15)
        )

        # Título do checklist

        ctk.CTkLabel(
            corpo,
            text="Título"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.campo_titulo = ctk.CTkEntry(
            corpo,
            height=38
        )

        self.campo_titulo.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Descrição

        ctk.CTkLabel(
            corpo,
            text="Descrição"
        ).grid(
            row=3,
            column=0,
            sticky="w"
        )

        self.campo_descricao = ctk.CTkTextbox(
            corpo,
            height=95
        )

        self.campo_descricao.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Prioridade

        ctk.CTkLabel(
            corpo,
            text="Prioridade"
        ).grid(
            row=5,
            column=0,
            sticky="w"
        )

        self.campo_prioridade = ctk.CTkOptionMenu(
            corpo,
            values=[
                "Baixa",
                "Média",
                "Alta"
            ]
        )

        self.campo_prioridade.grid(
            row=6,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Vencimento

        ctk.CTkLabel(
            corpo,
            text="Vencimento (DD/MM/AAAA)"
        ).grid(
            row=7,
            column=0,
            sticky="w"
        )

        self.campo_data = ctk.CTkEntry(
            corpo,
            height=38
        )

        self.campo_data.grid(
            row=8,
            column=0,
            sticky="ew",
            pady=(3, 18)
        )

        # Botões

        botoes = ctk.CTkFrame(
            corpo,
            fg_color="transparent"
        )

        botoes.grid(
            row=9,
            column=0,
            sticky="ew"
        )

        botoes.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("#182033", "#F1F5F9"),
            command=self.destroy
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 6)
        )

        ctk.CTkButton(
            botoes,
            text="Salvar checklist",
            command=self.salvar
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(6, 0)
        )

        # Valores iniciais

        self.campo_prioridade.set("Média")

        self.campo_data.insert(
            0,
            date.today().strftime("%d/%m/%Y")
        )

        # Se houver ID, preenche os campos existentes.

        if id_tarefa is not None:
            self.preencher()

        self.after(
            100,
            self.campo_titulo.focus_set
        )

    def preencher(self):

        tarefa = buscar_checklist(
            self.gerenciador,
            self.id_tarefa
        )

        self.campo_titulo.insert(
            0,
            tarefa.titulo
        )

        self.campo_descricao.insert(
            "1.0",
            tarefa.descricao
        )

        prioridades = {
            "BAIXA": "Baixa",
            "MEDIA": "Média",
            "ALTA": "Alta"
        }

        self.campo_prioridade.set(
            prioridades[tarefa.prioridade.name]
        )

        self.campo_data.delete(
            0,
            "end"
        )

        self.campo_data.insert(
            0,
            tarefa.data_vencimento.strftime(
                "%d/%m/%Y"
            )
        )

    def salvar(self):

        campos = (
            self.campo_titulo.get(),

            self.campo_descricao.get(
                "1.0",
                "end-1c"
            ),

            self.campo_prioridade.get(),

            self.campo_data.get()
        )

        try:

            if self.id_tarefa is None:

                tarefa = criar_checklist(
                    self.gerenciador,
                    *campos
                )

            else:

                tarefa = editar_checklist(
                    self.gerenciador,
                    self.id_tarefa,
                    *campos
                )

        except (ValueError, TypeError) as erro:

            messagebox.showwarning(
                "Dados inválidos",
                str(erro),
                parent=self
            )

            return

        except Exception as erro:

            messagebox.showerror(
                "Falha ao salvar",
                str(erro),
                parent=self
            )

            return

        self.destroy()

        self.ao_salvar(tarefa)