"""Janela de edição, conclusão, reabertura e exclusão de tarefa simples."""
from tkinter import messagebox

import customtkinter as ctk

from interface.gerenciamento import (
    alternar_conclusao_simples, buscar_simples, editar_simples, excluir_simples,
)


class JanelaDetalhes(ctk.CTkToplevel):
    def __init__(self, parent, gerenciador, id_tarefa: int, ao_alterar):
        super().__init__(parent)
        self.gerenciador = gerenciador
        self.id_tarefa = id_tarefa
        self.ao_alterar = ao_alterar
        self.title("Detalhes da tarefa simples")
        self.geometry("500x590")
        self.minsize(450, 560)
        self.transient(parent)
        self.grab_set()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.grid(row=0, column=0, sticky="nsew", padx=28, pady=22)
        corpo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(corpo, text="Detalhes da tarefa", font=ctk.CTkFont(size=23, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self.rotulo_estado = ctk.CTkLabel(corpo, text="", anchor="w")
        self.rotulo_estado.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        ctk.CTkLabel(corpo, text="Título", anchor="w").grid(row=2, column=0, sticky="ew")
        self.campo_titulo = ctk.CTkEntry(corpo, height=38)
        self.campo_titulo.grid(row=3, column=0, sticky="ew", pady=(3, 10))
        ctk.CTkLabel(corpo, text="Descrição", anchor="w").grid(row=4, column=0, sticky="ew")
        self.campo_descricao = ctk.CTkTextbox(corpo, height=95)
        self.campo_descricao.grid(row=5, column=0, sticky="ew", pady=(3, 10))
        ctk.CTkLabel(corpo, text="Prioridade", anchor="w").grid(row=6, column=0, sticky="ew")
        self.campo_prioridade = ctk.CTkOptionMenu(corpo, values=["Baixa", "Média", "Alta"], height=36)
        self.campo_prioridade.grid(row=7, column=0, sticky="ew", pady=(3, 10))
        ctk.CTkLabel(corpo, text="Vencimento (DD/MM/AAAA)", anchor="w").grid(row=8, column=0, sticky="ew")
        self.campo_data = ctk.CTkEntry(corpo, height=38)
        self.campo_data.grid(row=9, column=0, sticky="ew", pady=(3, 16))

        botoes = ctk.CTkFrame(corpo, fg_color="transparent")
        botoes.grid(row=10, column=0, sticky="ew")
        botoes.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(botoes, text="Salvar alterações", command=self.salvar).grid(
            row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        self.botao_estado = ctk.CTkButton(botoes, text="", command=self.alternar_estado)
        self.botao_estado.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")
        ctk.CTkButton(botoes, text="Excluir", fg_color="#B91C1C", hover_color="#991B1B",
                      command=self.excluir).grid(row=1, column=0, padx=(0, 5), pady=5, sticky="ew")
        ctk.CTkButton(botoes, text="Fechar", fg_color="transparent", border_width=1,
                      text_color=("#182033", "#F1F5F9"), command=self.destroy).grid(
            row=1, column=1, padx=(5, 0), pady=5, sticky="ew")
        self.carregar()

    def carregar(self):
        tarefa = buscar_simples(self.gerenciador, self.id_tarefa)
        self.campo_titulo.delete(0, "end")
        self.campo_titulo.insert(0, tarefa.titulo)
        self.campo_descricao.delete("1.0", "end")
        self.campo_descricao.insert("1.0", tarefa.descricao)
        self.campo_prioridade.set({"BAIXA": "Baixa", "MEDIA": "Média", "ALTA": "Alta"}[tarefa.prioridade.name])
        self.campo_data.delete(0, "end")
        self.campo_data.insert(0, tarefa.data_vencimento.strftime("%d/%m/%Y"))
        self.atualizar_estado(tarefa)

    def atualizar_estado(self, tarefa):
        self.rotulo_estado.configure(text="Situação: Concluída" if tarefa.concluida else "Situação: Pendente")
        self.botao_estado.configure(text="Reabrir" if tarefa.concluida else "Concluir")

    def salvar(self):
        try:
            tarefa = editar_simples(self.gerenciador, self.id_tarefa,
                                   self.campo_titulo.get(),
                                   self.campo_descricao.get("1.0", "end-1c"),
                                   self.campo_prioridade.get(), self.campo_data.get())
        except (ValueError, TypeError) as erro:
            messagebox.showwarning("Dados inválidos", str(erro), parent=self)
            return
        except Exception as erro:
            messagebox.showerror("Erro ao editar", str(erro), parent=self)
            return
        self.atualizar_estado(tarefa)
        self.ao_alterar()
        messagebox.showinfo("Tarefa atualizada", "Alterações salvas.", parent=self)

    def alternar_estado(self):
        try:
            tarefa = alternar_conclusao_simples(self.gerenciador, self.id_tarefa)
        except Exception as erro:
            messagebox.showerror("Erro ao atualizar situação", str(erro), parent=self)
            return
        self.atualizar_estado(tarefa)
        self.ao_alterar()

    def excluir(self):
        if not messagebox.askyesno("Confirmar exclusão",
                                   "Excluir esta tarefa permanentemente?", parent=self):
            return
        try:
            excluir_simples(self.gerenciador, self.id_tarefa)
        except Exception as erro:
            messagebox.showerror("Erro ao excluir", str(erro), parent=self)
            return
        self.destroy()
        self.ao_alterar()