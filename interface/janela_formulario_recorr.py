"""Janela de cadastro e edição de uma tarefa recorrente."""

from datetime import date
from tkinter import messagebox

import customtkinter as ctk

from interface.recorrencia_operacoes import (
    FREQUENCIAS,
    buscar_recorrente,
    criar_recorrente,
    editar_recorrente
)


class JanelaFormularioRecorr(ctk.CTkToplevel):

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
            "Editar recorrência"
            if id_tarefa is not None
            else "Nova recorrência"
        )

        self.geometry("510x640")
        self.minsize(470, 610)
        self.transient(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        corpo = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        corpo.grid(
            row=0,
            column=0,
            padx=24,
            pady=18,
            sticky="nsew"
        )

        corpo.grid_columnconfigure(0, weight=1)

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
            pady=(0, 14)
        )

        # Título

        ctk.CTkLabel(
            corpo,
            text="Título"
        ).grid(row=1, column=0, sticky="w")

        self.titulo = ctk.CTkEntry(corpo)

        self.titulo.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Descrição

        ctk.CTkLabel(
            corpo,
            text="Descrição"
        ).grid(row=3, column=0, sticky="w")

        self.descricao = ctk.CTkTextbox(
            corpo,
            height=85
        )

        self.descricao.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Prioridade

        ctk.CTkLabel(
            corpo,
            text="Prioridade"
        ).grid(row=5, column=0, sticky="w")

        self.prioridade = ctk.CTkOptionMenu(
            corpo,
            values=["Baixa", "Média", "Alta"]
        )

        self.prioridade.grid(
            row=6,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Vencimento

        ctk.CTkLabel(
            corpo,
            text="Vencimento (DD/MM/AAAA)"
        ).grid(row=7, column=0, sticky="w")

        self.vencimento = ctk.CTkEntry(corpo)

        self.vencimento.grid(
            row=8,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Frequência

        ctk.CTkLabel(
            corpo,
            text="Frequência"
        ).grid(row=9, column=0, sticky="w")

        self.frequencia = ctk.CTkOptionMenu(
            corpo,
            values=list(FREQUENCIAS)
        )

        self.frequencia.grid(
            row=10,
            column=0,
            sticky="ew",
            pady=(3, 12)
        )

        # Intervalo

        ctk.CTkLabel(
            corpo,
            text="Intervalo (inteiro maior que zero)"
        ).grid(row=11, column=0, sticky="w")

        self.intervalo = ctk.CTkEntry(corpo)

        self.intervalo.grid(
            row=12,
            column=0,
            sticky="ew",
            pady=(3, 16)
        )

        # Botões

        botoes = ctk.CTkFrame(
            corpo,
            fg_color="transparent"
        )

        botoes.grid(
            row=13,
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
            padx=(0, 6),
            sticky="ew"
        )

        ctk.CTkButton(
            botoes,
            text="Salvar",
            command=self.salvar
        ).grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="ew"
        )

        # Valores iniciais

        self.prioridade.set("Média")
        self.frequencia.set("Semanal")

        self.intervalo.insert(0, "1")

        self.vencimento.insert(
            0,
            date.today().strftime("%d/%m/%Y")
        )

        if id_tarefa is not None:
            self.preencher()

        self.after(100, self._ativar)

    def _ativar(self):

        if self.winfo_exists():
            self.grab_set()
            self.titulo.focus_set()

    def preencher(self):

        tarefa = buscar_recorrente(
            self.gerenciador,
            self.id_tarefa
        )

        self.titulo.insert(
            0,
            tarefa.titulo
        )

        self.descricao.insert(
            "1.0",
            tarefa.descricao
        )

        prioridades = {
            "BAIXA": "Baixa",
            "MEDIA": "Média",
            "ALTA": "Alta"
        }

        self.prioridade.set(
            prioridades[tarefa.prioridade.name]
        )

        self.vencimento.delete(
            0,
            "end"
        )

        self.vencimento.insert(
            0,
            tarefa.data_vencimento.strftime("%d/%m/%Y")
        )

        rotulo = next(
            rotulo
            for rotulo, valor in FREQUENCIAS.items()
            if valor == tarefa.recorrencia.frequencia
        )

        self.frequencia.set(rotulo)

        self.intervalo.delete(0, "end")

        self.intervalo.insert(
            0,
            str(tarefa.recorrencia.intervalo)
        )

    def salvar(self):

        campos = (
            self.titulo.get(),
            self.descricao.get("1.0", "end-1c"),
            self.prioridade.get(),
            self.vencimento.get(),
            self.frequencia.get(),
            self.intervalo.get()
        )

        try:

            if self.id_tarefa is None:

                tarefa = criar_recorrente(
                    self.gerenciador,
                    *campos
                )

            else:

                tarefa = editar_recorrente(
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