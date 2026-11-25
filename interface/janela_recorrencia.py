"""Janela de detalhes e gerenciamento de uma ocorrência recorrente."""

from tkinter import messagebox

import customtkinter as ctk

from interface.recorrencia_operacoes import (
    buscar_recorrente,
    alternar_conclusao,
    gerar_proxima,
    excluir_recorrente
)

from interface.janela_formulario_recorr import (
    JanelaFormularioRecorr
)


class JanelaRecorrencia(ctk.CTkToplevel):

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

        self.formulario = None

        self.title("Gerenciar recorrência")
        self.geometry("530x390")
        self.minsize(480, 360)

        self.transient(parent)
        self.grid_columnconfigure(0, weight=1)

        # Título

        self.titulo = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            ),
            wraplength=460
        )

        self.titulo.grid(
            row=0,
            column=0,
            padx=22,
            pady=(20, 8)
        )

        # Informações

        self.informacoes = ctk.CTkLabel(
            self,
            text="",
            justify="left"
        )

        self.informacoes.grid(
            row=1,
            column=0,
            padx=22,
            pady=(0, 18)
        )

        # Área dos botões

        acoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        acoes.grid(
            row=2,
            column=0,
            padx=22,
            sticky="ew"
        )

        acoes.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        # Concluir ou reabrir

        self.botao_estado = ctk.CTkButton(
            acoes,
            text="",
            command=self.mudar_estado
        )

        self.botao_estado.grid(
            row=0,
            column=0,
            padx=5,
            pady=6,
            sticky="ew"
        )

        # Gerar próxima ocorrência

        self.botao_proxima = ctk.CTkButton(
            acoes,
            text="Gerar próxima",
            command=self.gerar
        )

        self.botao_proxima.grid(
            row=0,
            column=1,
            padx=5,
            pady=6,
            sticky="ew"
        )

        # Editar

        ctk.CTkButton(
            acoes,
            text="Editar dados",
            command=self.editar
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=6,
            sticky="ew"
        )

        # Excluir

        ctk.CTkButton(
            acoes,
            text="Excluir",
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=self.excluir
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=6,
            sticky="ew"
        )

        # Fechar

        ctk.CTkButton(
            self,
            text="Fechar",
            fg_color="transparent",
            border_width=1,
            text_color=("#182033", "#F1F5F9"),
            command=self.destroy
        ).grid(
            row=3,
            column=0,
            pady=16
        )

        self.carregar()
        self.after(100, self._ativar)

    def _ativar(self):

        if self.winfo_exists():
            self.grab_set()

    def carregar(self):

        tarefa = buscar_recorrente(
            self.gerenciador,
            self.id_tarefa
        )

        self.titulo.configure(
            text=tarefa.titulo
        )

        situacao = (
            "Concluída"
            if tarefa.concluida
            else "Pendente"
        )

        self.informacoes.configure(
            text=(
                f"Descrição: {tarefa.descricao or '(sem descrição)'}\n"
                f"Prioridade: {tarefa.prioridade.name}\n"
                f"Vencimento: {tarefa.data_vencimento:%d/%m/%Y}\n"
                f"Recorrência: {tarefa.recorrencia}\n"
                f"Situação: {situacao}"
            )
        )

        self.botao_estado.configure(
            text=(
                "Reabrir"
                if tarefa.concluida
                else "Concluir"
            )
        )

        self.botao_proxima.configure(
            state=(
                "normal"
                if tarefa.concluida
                else "disabled"
            )
        )

    def executar(self, funcao):

        try:
            resultado = funcao()

        except (ValueError, TypeError) as erro:

            messagebox.showwarning(
                "Operação recusada",
                str(erro),
                parent=self
            )

            return

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self
            )

            return

        self.carregar()
        self.ao_alterar()

        return resultado

    def mudar_estado(self):

        self.executar(
            lambda: alternar_conclusao(
                self.gerenciador,
                self.id_tarefa
            )
        )

    def gerar(self):

        tarefa = self.executar(
            lambda: gerar_proxima(
                self.gerenciador,
                self.id_tarefa
            )
        )

        if tarefa is not None:

            messagebox.showinfo(
                "Ocorrência criada",
                (
                    f"Nova tarefa ID {tarefa.id}, "
                    f"vencimento "
                    f"{tarefa.data_vencimento:%d/%m/%Y}."
                ),
                parent=self
            )

    def editar(self):

        if (
            self.formulario is not None
            and self.formulario.winfo_exists()
        ):
            self.formulario.focus()
            return

        # Libera a janela atual para abrir o formulário modal.

        self.grab_release()

        self.formulario = JanelaFormularioRecorr(
            self,
            self.gerenciador,
            self.ao_editar,
            self.id_tarefa
        )

        self.formulario.bind(
            "<Destroy>",
            self._retomar
        )

    def _retomar(self, evento):

        if (
            evento.widget is self.formulario
            and self.winfo_exists()
        ):
            self.after(10, self.grab_set)

    def ao_editar(self, tarefa):

        self.carregar()
        self.ao_alterar()

    def excluir(self):

        confirmou = messagebox.askyesno(
            "Excluir tarefa",
            "Excluir esta ocorrência?",
            parent=self
        )

        if not confirmou:
            return

        try:

            excluir_recorrente(
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