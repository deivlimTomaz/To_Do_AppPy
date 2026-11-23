"""Janela de cadastro de tarefa simples."""
from datetime import date
from tkinter import messagebox

import customtkinter as ctk

from interface.cadastro import criar_tarefa_simples


class JanelaCadastro(ctk.CTkToplevel):
    def __init__(self, parent, gerenciador, ao_salvar):
        super().__init__(parent)
        self.gerenciador = gerenciador
        self.ao_salvar = ao_salvar

        self.title("Cadastrar tarefa simples")
        self.geometry("480x520")
        self.minsize(430, 490)
        self.transient(parent)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.grid(row=0, column=0, sticky="nsew", padx=28, pady=22)
        corpo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(corpo, text="Nova tarefa simples",
                     font=ctk.CTkFont(size=23, weight="bold"), anchor="w").grid(
                         row=0, column=0, sticky="ew", pady=(0, 18))

        ctk.CTkLabel(corpo, text="Título", anchor="w").grid(row=1, column=0, sticky="ew")
        self.campo_titulo = ctk.CTkEntry(corpo, placeholder_text="Ex.: Estudar Python", height=38)
        self.campo_titulo.grid(row=2, column=0, sticky="ew", pady=(4, 12))

        ctk.CTkLabel(corpo, text="Descrição", anchor="w").grid(row=3, column=0, sticky="ew")
        self.campo_descricao = ctk.CTkTextbox(corpo, height=100)
        self.campo_descricao.grid(row=4, column=0, sticky="ew", pady=(4, 12))

        ctk.CTkLabel(corpo, text="Prioridade", anchor="w").grid(row=5, column=0, sticky="ew")
        self.campo_prioridade = ctk.CTkOptionMenu(corpo, values=["Baixa", "Média", "Alta"], height=36)
        self.campo_prioridade.set("Média")
        self.campo_prioridade.grid(row=6, column=0, sticky="ew", pady=(4, 12))

        ctk.CTkLabel(corpo, text="Vencimento (DD/MM/AAAA)", anchor="w").grid(
            row=7, column=0, sticky="ew")
        self.campo_data = ctk.CTkEntry(corpo, height=38, placeholder_text="DD/MM/AAAA")
        self.campo_data.insert(0, date.today().strftime("%d/%m/%Y"))
        self.campo_data.grid(row=8, column=0, sticky="ew", pady=(4, 18))

        botoes = ctk.CTkFrame(corpo, fg_color="transparent")
        botoes.grid(row=9, column=0, sticky="ew")
        botoes.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(botoes, text="Cancelar", fg_color="transparent",
                      border_width=1, text_color=("#182033", "#F1F5F9"),
                      command=self.destroy).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.botao_salvar = ctk.CTkButton(botoes, text="Salvar tarefa", command=self.salvar)
        self.botao_salvar.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        self.after(100, self.campo_titulo.focus_set)

    def salvar(self):
        try:
            tarefa = criar_tarefa_simples(
                self.gerenciador,
                self.campo_titulo.get(),
                self.campo_descricao.get("1.0", "end-1c"),
                self.campo_prioridade.get(),
                self.campo_data.get(),
            )
        except (ValueError, TypeError) as erro:
            messagebox.showwarning("Dados inválidos", str(erro), parent=self)
            return
        except Exception as erro:
            messagebox.showerror("Erro ao salvar", f"Não foi possível gravar a tarefa.\n\n{erro}", parent=self)
            return

        self.destroy()
        self.ao_salvar(tarefa)
