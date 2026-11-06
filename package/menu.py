from package.gerenciador_tarefa import GerenciadorTarefa
from package.repositorio import Repositorio
import os
from package.prioridade import Prioridade
from datetime import datetime, date
from package.tarefa_simples import TarefaSimples
from package.tarefa_checklist import TarefaChecklist

class Menu:

    def __init__(self, gerenciador: GerenciadorTarefa, repositorio: Repositorio):
        self._gerenciador = gerenciador
        self._repositorio = repositorio


        # Menu pythônico em forma de dicionário
        # O número que o usuário digitar é justamente a chave que acessa os métodos
        self._opcoes = {
                "1": self.criar_tarefa, # Referência ao método criar_tarefa
                "2": self.listar_tarefas, # Referência ao método listar_tarefas
                "5": self.sair # Referência ao método sair
        }

        self._executando = True

    def mostrar_menu(self):

        while self._executando:
            
            self.limpar_tela()

            print("\n========== APP TO-DO ==========")
            print("1. Criar tarefa")
            print("2. Listar tarefas")
            print("5. Sair")
            print("=" * 31)

            opcao = input("Escolha uma opção: ").strip()
            
            # .get() pega a chave (número) escolhido pelo usuário e atribui à uma ação
            acao = self._opcoes.get(opcao)

            if acao is None:
                print("\nOpção inválida!")
                self.pausar()
                continue

            acao() # Chamada do método correspondente no dicionário somente após a validação da opção e escolha do usuário


    def criar_tarefa(self):
        
        submenu_criar = {
                "1": self._criar_simples,
                "2": self._criar_checklist,
                "3": self._criar_recorrente
        }

        while True:

            self.limpar_tela()

            print("\n========== CRIAR TAREFA ==========\n")
            print("1. Tarefa simples")
            print("2. Tarefa checklist")
            print("3. Tarefa recorrente")
            print("4. Voltar\n")
            print("=" * 34)
            opcao_criar = input("Escolha o tipo: ").strip()

            if opcao_criar == "4":
                break

            acao_criar = submenu_criar.get(opcao_criar)

            if acao_criar is None:
                print("\nOpção inválida")
                self.pausar()
                continue

            acao_criar()

            if not self._executando:
                break

    def _coletar_dados_comuns(self):
        
        # Solicitando dados

        while True:

            self.limpar_tela()

            titulo = input("Digite o título da tarefa: ").strip()
            
            if titulo:
                break
            
            print("O título não pode estar vazio!")

        
        descricao = input("\nDigite a descrição da tarefa: ").strip()
        
        print("\n========== PRIORIDADE ==========\n")
        print("1. Baixa")
        print("2. Média")
        print("3. Alta\n")
        

        opcoes_prioridade = {
                "1": Prioridade.BAIXA,
                "2": Prioridade.MEDIA,
                "3": Prioridade.ALTA
        }

        while True:
            opcao_prioridade = input("Escolha: ").strip()
        
            acao_prioridade = opcoes_prioridade.get(opcao_prioridade)

            if acao_prioridade is None:
                print("\nOpção inválida")
                continue

            break

        while True:
            data = input("\nDigite a data de vencimento da tarefa (DD/MM/AAAA): ")
            
            try:
                data = datetime.strptime(data, "%d/%m/%Y").date()

            except ValueError:
                print("\nData inválida! Informe uma data válida.")
                continue

            if data < date.today():
                print("\nData passada! Informe uma data a partir de hoje.")
                continue
            break

        return {
                "titulo": titulo,
                "descricao": descricao,
                "prioridade": acao_prioridade,
                "data_vencimento": data
        }
        
    def _criar_simples(self):

        dados_comuns = self._coletar_dados_comuns() # Chamar método de solicitação de dados
        tarefa_id = self._gerenciador.gerar_id() # Gerenciador de tarefas cria um id para determinada tarefa

        tarefa_simples = TarefaSimples(tarefa_id, **dados_comuns) # Tarefa recebe as características completas de uma tarefa simples + seu id + dados comuns
        self._gerenciador.criar(tarefa_simples) # Gerenciador cadastra essa tarefa no sistema

        print("\nTarefa simples criada com sucesso!")
        self.pausar()

    def _criar_checklist(self):
        
        dados_comuns = self._coletar_dados_comuns()
        tarefa_id = self._gerenciador.gerar_id()

        tarefa_checklist = TarefaChecklist(tarefa_id, **dados_comuns)

        while True:
            add_item = input("\nDeseja adicionar um item? (S/N): ").strip().lower()
            if add_item == "s":
                item = input("\nDigite o item: ").strip()
                if not item:
                    print("\nO item não pode estar vazio!")
                    continue
                tarefa_checklist.adicionar_item(item)
            elif add_item == "n":
                break
            else:
                print("\nDigite apenas sim ou não.")
            
        self._gerenciador.criar(tarefa_checklist)
        
        print("\nTarefa checklist criada com sucesso!")
        self.pausar()

    # Exibição específica de itens checklist para o usuário
    def _exibir_checklist(self, tarefa: TarefaChecklist):
        
        print("\nChecklist:")
        itens = tarefa.itens

        for item in itens:
            if not item.feito:
                print(f"    [ ] - {item.texto}")
            else:
                print(f"    [x] - {item.texto}")
            
        total = len(itens)

        concluidos = sum(item.feito for item in itens)

        print(f"\nProgresso: {concluidos}/{total} itens concluídos")

    def _criar_recorrente(self):
        pass

    def listar_tarefas(self):
        
        tarefas = self._gerenciador.lista.tarefas

        if not tarefas:
            print("\nNenhuma tarefa cadastrada!")
            self.pausar()
            return

        print("\n========== SUAS TAREFAS ==========")
        
        for tarefa in tarefas:
            
            status = "Concluída" if tarefa.concluida else "Pendente"
            
            # Atributos comuns a todas as tarefas

            print(f"\nID: {tarefa.id}")
            print(f"Título: {tarefa.titulo}")
            print(f"Prioridade: {tarefa.prioridade.name}")
            print(f"Vencimento: {tarefa.data_vencimento}")
            print(f"Status: {status}")

            if isinstance(tarefa, TarefaChecklist):
                 self._exibir_checklist(tarefa)
            
            print("-" * 35)
        
        if self._executando:
            self.pausar()

    def sair(self):
        print("\nEncerrando o aplicativo...")
        self._executando = False

    def pausar(self):
        input("\nPressione ENTER para continuar....")

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear") # Ação para limpar tela do terminal deixando mais organizado. "cls" para windows e "clear" para unix
