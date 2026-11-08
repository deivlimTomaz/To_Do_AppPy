from package.gerenciador_tarefa import GerenciadorTarefa
from package.repositorio import Repositorio
import os
from package.prioridade import Prioridade
from datetime import datetime, date
from package.tarefa import Tarefa
from package.tarefa_simples import TarefaSimples
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.recorrencia import Recorrencia

class Menu:

    def __init__(self, gerenciador: GerenciadorTarefa, repositorio: Repositorio):
        self._gerenciador = gerenciador
        self._repositorio = repositorio


        # Menu pythônico em ma de dicionário
        # O número que o usuário digitar é justamente a chave que acessa os métodos
        self._opcoes = {
                "1": self.criar_tarefa, # Referência ao método criar_tarefa
                "2": self.listar_tarefas, # Referência ao método listar_tarefas
                "3": self.editar_tarefa,
                "5": self.sair # Referência ao método sair
        }

        self._executando = True

    def mostrar_menu(self):

        while self._executando:

            self.limpar_tela()

            print("\n========== APP TO-DO ==========")
            print("1. Criar tarefa")
            print("2. Listar tarefas")
            print("3. Editar tarefa")
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
        dados_comuns = self._coletar_dados_comuns()

        print("\n========== FREQUÊNCIA ==========\n")
        print("1. Diária")
        print("2. Semanal")
        print("3. Mensal")
        print("4. Anual\n")

        opcoes_frequencia = {
            "1": "diaria",
            "2": "semanal",
            "3": "mensal",
            "4": "anual"
        }

        while True:
            opcao_frequencia = input("Escolha: ").strip()

            frequencia = opcoes_frequencia.get(opcao_frequencia)

            if frequencia is None:
                print("\nOpção inválida")
                continue
            break

        while True:
            try:
                intervalo = int(input("\nDigite o intervalo de tempo para a tarefa: "))
                if intervalo <= 0:
                    print("O intervalo deve ser maior que zero!")
                    continue
                break

            except ValueError:
                print("\nInforme um número inteiro válido.")

        # Construção da recorrência
        recorr = Recorrencia(frequencia, intervalo)

        tarefa_id = self._gerenciador.gerar_id()

        tarefa_recorr = TarefaRecorr(tarefa_id, **dados_comuns, recorr=recorr)

        # Cadastro
        self._gerenciador.criar(tarefa_recorr)

        print("\nTarefa recorrente criada com sucesso!")
        self.pausar()

    def _exibir_recorr(self, tarefa: TarefaRecorr):

        print("\nRecorrência:")
        recorr = tarefa.recorrencia

        unidades = {
            "diaria": ("dia", "dias"),
            "semanal": ("semana", "semanas"),
            "mensal": ("mês", "meses"),
            "anual": ("ano", "anos")
        }

        singular, plural = unidades[recorr.frequencia]

        unidade = singular if recorr.intervalo == 1 else plural

        print(f"Frequência: {recorr.frequencia.capitalize()}")
        print(f"Intervalo: A cada {recorr.intervalo} {unidade}")

    def listar_tarefas(self):

        tarefas = self._gerenciador.lista.tarefas

        if not tarefas:
            print("\nNenhuma tarefa cadastrada!")
            self.pausar()
            return

        self.limpar_tela()

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

            if isinstance(tarefa, TarefaRecorr):
                self._exibir_recorr(tarefa)

            print("-" * 35)

        if self._executando:
            self.pausar()

    def _listar_tarefas_resumidas(self):
        tarefas = self._gerenciador.lista.tarefas

        self.limpar_tela()

        print("\n========== SELECIONAR TAREFA ==========")

        for tarefa in tarefas:
            print(f"[{tarefa.id}] - {tarefa.titulo}")

        print("-" * 35)

    def editar_tarefa(self):
        tarefas = self._gerenciador.lista.tarefas

        if not tarefas:
            print("\nNenhuma tarefa cadastrada!")
            self.pausar()
            return

        self._listar_tarefas_resumidas()

        while True:

            try:
                id_tarefa = int(input("\nDigite o ID da tarefa (0 para voltar): "))

            except ValueError:
                print("\nInforme um número inteiro válido")
                continue

            if id_tarefa == 0:
                return

            if id_tarefa < 0:
                print("\nInforme um ID positivo!")
                continue

            try:
                tarefa = self._gerenciador.buscar_por_id(id_tarefa)
            except ValueError:
                print(f"\nNenhuma tarefa foi encontrada com o ID {id_tarefa}!")
                continue

            print(f"\nTarefa selecionada: {tarefa.titulo}")
            break

        # =========================================================
        #               PARTE DO SUBMENU EDITAR
        # =========================================================

        submenu_editar = {
            "1": self._alterar_titulo,
            "2": self._alterar_descricao,
            "3": self._alterar_prioridade,
            "4": self._alterar_vencimento,
            "9": self._concluir_tarefa,
            "10": self._excluir_tarefa,
        }

        if isinstance(tarefa, TarefaChecklist):
            submenu_editar["5"] = self._gerenciar_checklist
            submenu_editar["6"] = self._adicionar_item_checklist
            submenu_editar["7"] = self._desmarcar_item_checklist

        if isinstance(tarefa, TarefaRecorr):
            submenu_editar["8"] = self._gerar_proxima_recorrencia

        while True:

            self.limpar_tela()

            print("\n========== EDITAR TAREFA ==========")
            print("\n1. Alterar título")
            print("2. Alterar descrição")
            print("3. Alterar prioridade")
            print("4. Alterar vencimento")
            if isinstance(tarefa, TarefaChecklist):
                print("5. Gerenciar checklist")
                print("6. Adicionar item ao checklist")
                print("7. Desmarcar item do checklist")
            if isinstance(tarefa, TarefaRecorr):
                print("8. Gerar próxima ocorrência da tarefa")
            print("9. Concluir tarefa")
            print("10. Excluir tarefa")
            print("11. Voltar\n")
            print("=" * 34)

            opcao_editar = input("O que deseja fazer? ").strip()

            if opcao_editar == "11":
                break

            acao_editar = submenu_editar.get(opcao_editar)

            if acao_editar is None:
                print("\nOpção inválida")
                self.pausar()
                continue

            resultado = acao_editar(tarefa)

            if opcao_editar == "10" and resultado is True:
                break

    def _alterar_titulo(self, tarefa: Tarefa):

        self.limpar_tela()

        print("\n========== ALTERAR TÍTULO ==========")
        print(f"\nTítulo atual: {tarefa.titulo}")

        while True:

            novo_titulo = input("\nDigite o novo título: ").strip()

            if novo_titulo:
                break

            print("O título não pode estar vazio!")

        tarefa_editada = self._gerenciador.editar(tarefa, novo_titulo, tarefa.descricao, tarefa.prioridade, tarefa.data_vencimento)

        print("\nTarefa editada com sucesso!")
        self.pausar()

    def _alterar_descricao(self, tarefa: Tarefa):

        self.limpar_tela()

        print("\n========== ALTERAR DESCRIÇÃO ==========")
        print(f"\nDescrição atual: {tarefa.descricao}")

        nova_descricao = input("\nDigite uma nova descriçao: ").strip()

        tarefa_editada = self._gerenciador.editar(tarefa, tarefa.titulo, nova_descricao, tarefa.prioridade, tarefa.data_vencimento)

        print("\nTarefa editada com sucesso")
        self.pausar()


    def _alterar_prioridade(self, tarefa: Tarefa):

        self.limpar_tela()
        print("\n========== ALTERAR PRIORIDADE ==========")
        print(f"\nPrioridade atual: {tarefa.prioridade.name}")

        print("\n========== PRIORIDADES DISPONÍVEIS ==========\n")
        print("1. Baixa")
        print("2. Média")
        print("3. Alta\n")

        opcoes_prioridade = {
                "1": Prioridade.BAIXA,
                "2": Prioridade.MEDIA,
                "3": Prioridade.ALTA
        }

        while True:
            opcao_prioridade = input("Escolha uma nova prioridade: ").strip()

            nova_prioridade = opcoes_prioridade.get(opcao_prioridade)

            if nova_prioridade is None:
                print("\nOpção inválida")
                continue

            break

        self._gerenciador.editar(tarefa, tarefa.titulo, tarefa.descricao, nova_prioridade, tarefa.data_vencimento)

        print("\nTarefa editada com sucesso!")
        self.pausar()


    def _alterar_vencimento(self, tarefa: Tarefa):
        self.limpar_tela()
        data_atual = tarefa.data_vencimento.strftime("%d/%m/%Y")

        print("\n========== ALTERAR DATA DE VENCIMENTO ==========")
        print(f"\nData de vencimento atual: {data_atual}")

        while True:
            data_venc = input("Escolha uma nova data de vencimento: ")

            try:
                nova_data_venc = datetime.strptime(data_venc,"%d/%m/%Y").date()
            except ValueError:
                print("\nData inválida! Informe uma data válida.")
                continue

            if nova_data_venc < date.today():
                print("\nData passada! Informe uma data a partir de hoje.")
                continue
            break

        self._gerenciador.editar(tarefa, tarefa.titulo, tarefa.descricao, tarefa.prioridade, nova_data_venc)

        print("\nTarefa editada com sucesso!")
        self.pausar()

    def _gerenciar_checklist(self, tarefa: TarefaChecklist):

        if not isinstance(tarefa, TarefaChecklist):
            print("\nEsta tarefa não é do tipo checklist!")
            self.pausar()
            return

        if tarefa.concluida:
            print("\nReabra a tarefa antes de modificar os itens!")
            self.pausar()
            return

        self.limpar_tela()

        print("\n========== GERENCIAR CHECKLIST ==========")
        print(f"Tarefa: {tarefa.titulo}")

        itens = tarefa.itens

        if not itens:
            print("\nEste checklist não possui itens cadastrados.")
            self.pausar()
            return

        for numero, item in enumerate(tarefa.itens, start=1):
            status = "[x]" if item.feito else "[ ]"
            print(f"{numero}. {status} {item.texto}")

        while True:
            try:
                numero_item = int(input("\nDigite o número do item (0 para voltar): "))

            except ValueError:
                print("\nNúmero inválido.")
                continue

            if numero_item == 0:
                return

            if numero_item < 1 or numero_item > len(tarefa.itens):
                print("\nEsse item não existe!")
                continue
            break

        indice = numero_item - 1

        try:
            tarefa.marcar_item(indice)

        except ValueError as erro:
            print(f"\nNão foi possível marcar o item: {erro}")
            self.pausar()
            return

        print("\nItem marcado com sucesso!")
        self.pausar()

    def _adicionar_item_checklist(self, tarefa: TarefaChecklist):

        if tarefa.concluida:
            print("\nReabra a tarefa antes de modificar os itens!")
            self.pausar()
            return

        self.limpar_tela()

        print("\n========== ADICIONAR ITEM ==========")
        print(f"\nTarefa: {tarefa.titulo}")

        while True:
            novo_item = input("\nDigite o novo item (0 para voltar): ").strip()

            if novo_item == "0":
                return

            if not novo_item:
                print("\nO item não pode estar vazio!")
                continue

            try:
                tarefa.adicionar_item(novo_item)
            except ValueError as erro:
                print(f"\nNão foi possível adicionar o item: {erro}")
                self.pausar()
                return

            print("\nItem adicionado com sucesso!")
            self.pausar()
            return

    def _desmarcar_item_checklist(self, tarefa: TarefaChecklist):

        if tarefa.concluida:
            print("\nReabra a tarefa antes de modificar os itens!")
            self.pausar()
            return

        self.limpar_tela()

        print("\n========== DESMARCAR ITEM ==========")
        print(f"\nTarefa: {tarefa.titulo}")

        itens = tarefa.itens

        if not itens:
            print("\nEste checklist não possui itens!")
            self.pausar()
            return

        for numero, item in enumerate(itens, start=1):
            status = "[x]" if item.feito else "[ ]"
            print(f"{numero}. {status} {item.texto}")

        while True:
            try:
                numero_item = int(input("\nDigite o número do item (0 para voltar): "))
            except ValueError:
                print("\nInforme um número inteiro válido!")
                continue

            if numero_item == 0:
                return

            if numero_item < 1 or numero_item > len(itens):
                print("\nEsse item não existe!")
                continue

            item_selecionado = itens[numero_item - 1]

            if not item_selecionado.feito:
                print("\nEsse item já está desmarcado!")
                continue

            try:
                item_selecionado.desmarcar()
            except ValueError as erro:
                print(f"\nNão foi possível desmarcar o item: {erro}")
                self.pausar()
                return

            print("\nItem desmarcado com sucesso!")
            self.pausar()
            return

    def _gerar_proxima_recorrencia(self, tarefa: TarefaRecorr):

        self.limpar_tela()

        print("\n========== GERAR PRÓXIMA RECORRÊNCIA ==========")
        print(f"\nTarefa: {tarefa.titulo}")
        print(f"\nFrequência: {tarefa.recorrencia.frequencia.capitalize()}")
        print(f"\nStatus: {'Concluída' if tarefa.concluida else 'Pendente'}\n")

        if not tarefa.concluida:
            print("\nConclua a tarefa antes de gerar a próxima ocorrência")
            self.pausar()
            return

        while True:

            decisao_recorr = input("\nGerar próxima recorrência (S/N)? ").strip().lower()

            if decisao_recorr == 's':
                try:
                    novo_id = self._gerenciador.gerar_id()
                    nova_tarefa = tarefa.gerar_proxima(novo_id)
                    self._gerenciador.criar(nova_tarefa)

                except ValueError as erro:
                    print(f"\nNão foi possível gerar a ocorrência: {erro}")
                    self.pausar()
                    return

                print("\nNova ocorrência criada com sucesso!")
                print(f"\nNovo ID: {nova_tarefa.id}")
                print(f"\nNovo vencimento: " f"{nova_tarefa.data_vencimento.strftime('%d/%m/%Y')}")

                self.pausar()
                return

            elif decisao_recorr == 'n':
                return
            else:
                print("Digite S ou N.")

    def _concluir_tarefa(self, tarefa: Tarefa):
        self.limpar_tela()

        if tarefa.concluida:
            print("\nEssa tarefa já está concluída!")
            self.pausar()
            return

        print("\n========== CONCLUIR TAREFA ==========")
        print(f"\nTarefa selecionada: {tarefa.titulo}")
        print(f"Status atual: {'Concluída' if tarefa.concluida else 'Pendente'}\n")

        while True:
            decisao_concluir = input("Deseja concluir esta tarefa (S/N)? ").strip().lower()

            if decisao_concluir == 's':
                try:
                    self._gerenciador.concluir(tarefa)

                except ValueError as erro:
                    print(f"\nNão foi possível concluir esta tarefa: {erro}")
                    self.pausar()
                    return

                print("\nTarefa concluída com sucesso!")
                self.pausar()
                return

            elif decisao_concluir == 'n':
                return
            else:
                print("\nResposta inválida.")

    def _excluir_tarefa(self, tarefa: Tarefa):
        self.limpar_tela()

        print("\n========== EXCLUIR TAREFA ==========")
        print(f"\nTarefa: {tarefa.titulo}")

        while True:
            decisao_excluir = input("Deseja realmente excluir esta tarefa (S/N)? ").strip().lower()

            if decisao_excluir == 's':
                try:
                    self._gerenciador.excluir(tarefa)

                except ValueError as erro:
                    print(f"\nNão foi possível excluir esta tarefa: {erro}")
                    self.pausar()
                    return False

                print("\nTarefa excluída com sucesso!")
                self.pausar()
                return True

            elif decisao_excluir == 'n':
                return False

            else:
                print("\nResposta inválida.")

    def sair(self):
        print("\nEncerrando o aplicativo...")
        self._executando = False

    def pausar(self):
        input("\nPressione ENTER para continuar....")

    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear") # Ação para limpar tela do terminal deixando mais organizado. "cls" para windows e "clear" para unix
