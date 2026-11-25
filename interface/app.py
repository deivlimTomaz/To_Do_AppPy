import customtkinter as ctk

from tkinter import messagebox

from package.gerenciador_tarefa import GerenciadorTarefa
from package.tarefa_simples import TarefaSimples
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr

from interface.tarefas_view import (
    filtrar_tarefas,
    resumo_tarefa
)

from interface.janela_cadastro import JanelaCadastro
from interface.janela_detalhes import JanelaDetalhes
from interface.janela_checklist import JanelaChecklist

from interface.janela_formulario_checklist import (
    JanelaFormularioChecklist
)

from interface.janela_formulario_recorr import (JanelaFormularioRecorr)
from interface.janela_recorrencia import(JanelaRecorrencia)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self, gerenciador: GerenciadorTarefa):

        if not isinstance(gerenciador, GerenciadorTarefa):
            raise TypeError(
                "App precisa de um GerenciadorTarefa"
            )

        super().__init__()

        self.gerenciador = gerenciador

        self.secao_atual = "Tarefas"
        self.botoes_navegacao = {}

        self.janela_cadastro = None
        self.janela_detalhes = None
        self.janela_checklist = None
        self.janela_formulario_checklist = None
        self.janela_formulario_recorr = None
        self.janela_recorrencia = None

        self.title(
            "To-Do App | Gerenciador de Tarefas"
        )

        self.geometry("1100x700")
        self.minsize(850, 550)

        # Cores: tema claro, tema escuro

        self.cor_fundo = ("#F3F5F9", "#17191F")
        self.cor_sidebar = ("#FFFFFF", "#1E222B")
        self.cor_card = ("#FFFFFF", "#262A33")
        self.cor_texto = ("#182033", "#F1F5F9")
        self.cor_secundaria = ("#64748B", "#A9B0BD")
        self.cor_selecionada = ("#DBEAFE", "#303A50")

        self.configure(
            fg_color=self.cor_fundo
        )

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_conteudo()

        self.mostrar_secao("Tarefas")

    def criar_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=self.cor_sidebar
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="☑  To-Do App",
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            ),
            text_color=self.cor_texto
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(35, 40)
        )

        secoes = [
            ("Tarefas", "☷  Tarefas"),
            ("Checklists", "☑  Checklists"),
            ("Recorrentes", "↻  Recorrentes")
        ]

        for indice, (nome, texto) in enumerate(
            secoes,
            start=1
        ):

            botao = ctk.CTkButton(
                self.sidebar,
                text=texto,
                height=43,
                corner_radius=8,
                anchor="w",
                fg_color="transparent",
                hover_color=self.cor_selecionada,
                text_color=self.cor_texto,
                font=ctk.CTkFont(size=14),
                command=lambda secao=nome: (
                    self.mostrar_secao(secao)
                )
            )

            botao.grid(
                row=indice,
                column=0,
                padx=15,
                pady=5,
                sticky="ew"
            )

            self.botoes_navegacao[nome] = botao

        ctk.CTkLabel(
            self.sidebar,
            text="Aparência",
            text_color=self.cor_secundaria,
            anchor="w"
        ).grid(
            row=6,
            column=0,
            padx=20,
            pady=(10, 5),
            sticky="ew"
        )

        self.menu_tema = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Escuro", "Claro"],
            command=self.alterar_tema,
            height=35
        )

        self.menu_tema.set("Escuro")

        self.menu_tema.grid(
            row=7,
            column=0,
            padx=20,
            pady=(0, 30),
            sticky="ew"
        )

    def criar_conteudo(self):

        self.conteudo = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )

        self.conteudo.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=30
        )

        self.conteudo.grid_columnconfigure(0, weight=1)
        self.conteudo.grid_rowconfigure(1, weight=1)

        cabecalho = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )

        cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 25)
        )

        cabecalho.grid_columnconfigure(0, weight=1)

        self.titulo_secao = ctk.CTkLabel(
            cabecalho,
            text="Minhas tarefas",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            ),
            text_color=self.cor_texto
        )

        self.titulo_secao.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.botao_atualizar = ctk.CTkButton(
            cabecalho,
            text="Atualizar",
            width=100,
            height=40,
            fg_color="transparent",
            border_width=1,
            border_color=("#CBD5E1", "#475569"),
            text_color=self.cor_texto,
            command=self.atualizar_lista
        )

        self.botao_atualizar.grid(
            row=0,
            column=1,
            padx=(8, 12)
        )

        self.botao_novo = ctk.CTkButton(
            cabecalho,
            text="+ Nova tarefa",
            width=150,
            height=40,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.nova_tarefa
        )

        self.botao_novo.grid(
            row=0,
            column=2,
            sticky="e"
        )

        self.lista = ctk.CTkScrollableFrame(
            self.conteudo,
            fg_color="transparent"
        )

        self.lista.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.lista.grid_columnconfigure(0, weight=1)

    def mostrar_secao(self, secao):

        self.secao_atual = secao

        for nome, botao in self.botoes_navegacao.items():

            if nome == secao:

                botao.configure(
                    fg_color=self.cor_selecionada,
                    text_color=("#1D4ED8", "#93C5FD")
                )

            else:

                botao.configure(
                    fg_color="transparent",
                    text_color=self.cor_texto
                )

        titulos = {
            "Tarefas": "Minhas tarefas",
            "Checklists": "Meus checklists",
            "Recorrentes": "Tarefas recorrentes"
        }

        self.titulo_secao.configure(
            text=titulos[secao]
        )

        textos_botoes = {
            "Tarefas": "+ Nova tarefa",
            "Checklists": "+ Novo checklist",
            "Recorrentes": "+ Nova recorrência"
        }

        # Altera o botão de acordo com a seção.

        self.botao_novo.configure(text = textos_botoes[secao])

        self.atualizar_lista()

    def atualizar_lista(self):

        try:

            tarefas = self.gerenciador.listar()

            tarefas_visiveis = filtrar_tarefas(
                tarefas,
                self.secao_atual
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao carregar tarefas",
                (
                    "Não foi possível consultar "
                    f"o banco de dados.\n\n{erro}"
                ),
                parent=self
            )

            return

        for widget in self.lista.winfo_children():
            widget.destroy()

        if not tarefas_visiveis:

            ctk.CTkLabel(
                self.lista,
                text="Nenhuma tarefa cadastrada nesta seção.",
                font=ctk.CTkFont(size=15),
                text_color=self.cor_secundaria
            ).grid(
                row=0,
                column=0,
                pady=60
            )

            return

        for indice, tarefa in enumerate(tarefas_visiveis):

            self.criar_card(
                resumo_tarefa(tarefa),
                indice
            )

    def criar_card(self, dados, linha):

        card = ctk.CTkFrame(
            self.lista,
            fg_color=self.cor_card,
            corner_radius=12
        )

        card.grid(
            row=linha,
            column=0,
            sticky="ew",
            padx=5,
            pady=(0, 12)
        )

        card.grid_columnconfigure(1, weight=1)

        estado = (
            "☑"
            if dados["concluida"]
            else "☐"
        )

        ctk.CTkLabel(
            card,
            text=estado,
            font=ctk.CTkFont(size=25),
            text_color=("#2563EB", "#93C5FD")
        ).grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(20, 15)
        )

        ctk.CTkLabel(
            card,
            text=dados["titulo"],
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=self.cor_texto,
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=(16, 0)
        )

        situacao = (
            "Concluída"
            if dados["concluida"]
            else "Pendente"
        )

        if dados["atrasada"]:
            situacao = "Atrasada"

        detalhes = (
            f"Prioridade: {dados['prioridade']}  |  "
            f"Vence: {dados['vencimento']}  |  "
            f"{situacao}"
        )

        ctk.CTkLabel(
            card,
            text=detalhes,
            font=ctk.CTkFont(size=12),
            text_color=self.cor_secundaria,
            anchor="w"
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            pady=(0, 16)
        )

        ctk.CTkButton(
            card,
            text="Detalhes",
            width=85,
            height=32,
            fg_color="transparent",
            border_width=1,
            border_color=("#CBD5E1", "#475569"),
            text_color=self.cor_texto,
            command=lambda id_tarefa=dados["id"]: (
                self.abrir_detalhes(id_tarefa)
            )
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=20
        )

    def alterar_tema(self, escolha):

        modo = (
            "dark"
            if escolha == "Escuro"
            else "light"
        )

        ctk.set_appearance_mode(modo)

    def nova_tarefa(self):

        # Cadastro de checklist

        if self.secao_atual == "Checklists":

            if (
                self.janela_formulario_checklist is not None
                and self.janela_formulario_checklist.winfo_exists()
            ):
                self.janela_formulario_checklist.focus()
                return

            self.janela_formulario_checklist = (
                JanelaFormularioChecklist(
                    self,
                    self.gerenciador,
                    self.ao_cadastrar_checklist
                )
            )

            return

        # Cadastro de recorrências

        if self.secao_atual == "Recorrentes":
            if (self.janela_formulario_recorr is not None and self.janela_formulario_recorr.winfo_exists()):
                self.janela_formulario_recorr.focus()
                return

            self.janela_formulario_recorr = (
                JanelaFormularioRecorr(
                    self, self.gerenciador, self.ao_cadastrar_recorrente
                )
            )

            return

        # Cadastro de tarefa simples

        if (
            self.janela_cadastro is not None
            and self.janela_cadastro.winfo_exists()
        ):
            self.janela_cadastro.focus()
            return

        self.janela_cadastro = JanelaCadastro(
            self,
            self.gerenciador,
            self.ao_cadastrar_tarefa
        )

    def ao_cadastrar_checklist(self, tarefa):

        self.mostrar_secao("Checklists")

        # Abre a janela para adicionar itens ao checklist.

        self.abrir_detalhes(tarefa.id)

    def ao_cadastrar_tarefa(self, tarefa):

        self.mostrar_secao("Tarefas")

    def abrir_detalhes(self, id_tarefa):

        try:
            tarefa = self.gerenciador.buscar_por_id(
                id_tarefa
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro ao abrir tarefa",
                str(erro),
                parent=self
            )

            return

        # Checklist

        if isinstance(tarefa, TarefaChecklist):

            if (
                self.janela_checklist is not None
                and self.janela_checklist.winfo_exists()
            ):
                self.janela_checklist.focus()
                return

            self.janela_checklist = JanelaChecklist(
                self,
                self.gerenciador,
                id_tarefa,
                self.atualizar_lista
            )

            return

        # Tarefa recorrente

        if isinstance(tarefa, TarefaRecorr):

            if (
                self.janela_recorrencia is not None
                and self.janela_recorrencia.winfo_exists()
            ):
                self.janela_recorrencia.focus()
                return

            self.janela_recorrencia = JanelaRecorrencia(
                self,
                self.gerenciador,
                id_tarefa,
                self.atualizar_lista
            )

            return

        # Tarefa simples

        if isinstance(tarefa, TarefaSimples):

            if (
                self.janela_detalhes is not None
                and self.janela_detalhes.winfo_exists()
            ):
                self.janela_detalhes.focus()
                return

            self.janela_detalhes = JanelaDetalhes(
                self,
                self.gerenciador,
                id_tarefa,
                self.atualizar_lista
            )

            return

        messagebox.showerror(
            "Tipo não suportado",
            "O tipo da tarefa não foi reconhecido.",
            parent=self
        )

    def executar(self):
        self.mainloop()

    def ao_cadastrar_recorrente(self, tarefa):

        self.mostrar_secao("Recorrentes")

        self.abrir_detalhes(tarefa.id)


if __name__ == "__main__":

    raise SystemExit(
        "Execute a aplicação pelo arquivo main_gui.py"
    )