"""Demonstração funcional para o vídeo do Nível 1.

Coloque este arquivo na raiz do projeto, ao lado da pasta package.
Execute: python demonstracao_nivel1.py
"""

from datetime import date, timedelta
from pprint import pprint

from package.categoria import Categoria
from package.gerenciador_tarefa import GerenciadorTarefa
from package.lista import Lista
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.tarefa_simples import TarefaSimples

# Datas futuras evitam que o exemplo fique desatualizado.
data_futura = date.today() + timedelta(days=7)

print('\n========== 1. LISTAS E CATEGORIAS (ASSOCIAÇÃO) ==========')
categoria = Categoria('azul', 'Estudos')
lista = Lista('Faculdade', categoria)
outra_lista = Lista('Cursos', categoria)
gerenciador = GerenciadorTarefa(lista)
print('Lista:', lista.nome)
print('Categoria da lista:', lista.categoria.tipo, '-', lista.categoria.cor)
print('Outra lista:', outra_lista.nome)
print('Categoria da outra lista:', outra_lista.categoria.tipo)

print('\n========== 2. CRIANDO DIFERENTES TIPOS DE TAREFA (HERANÇA) ==========')
simples = TarefaSimples(1, 'Ler capítulo', 'Ler material da disciplina', Prioridade.BAIXA, data_futura)
checklist = TarefaChecklist(2, 'Preparar apresentação', 'Organizar demonstração', Prioridade.ALTA, data_futura)
recorrente = TarefaRecorr(3, 'Praticar Python', 'Prática semanal', Prioridade.MEDIA,
                         date.today(), Recorrencia('semanal', 1))

gerenciador.criar(simples)
gerenciador.criar(checklist)
gerenciador.criar(recorrente)
for tarefa in lista.tarefas:
    print(f'{type(tarefa).__name__}: {tarefa.para_dict()["titulo"]} | vencimento: {tarefa.data_vencimento}')

print('\n========== 3. CHECKLIST E ITENS (COMPOSIÇÃO) ==========')
checklist.adicionar_item('Revisar UML')
checklist.adicionar_item('Executar demonstração')
print('Checklist antes de marcar os itens:')
pprint(checklist.para_dict())
print('Tentando concluir com itens pendentes...')
try:
    gerenciador.concluir(checklist)
except ValueError as erro:
    print('O sistema impediu a conclusão:', erro)

checklist.marcar_item(0)
checklist.marcar_item(1)
print('Checklist após marcar os itens:')
pprint(checklist.para_dict())

print('\n========== 4. CONCLUINDO DIFERENTES TAREFAS (POLIMORFISMO) ==========')
for tarefa in (simples, checklist, recorrente):
    print(f'Antes: {type(tarefa).__name__} | concluída: {tarefa.para_dict()["concluida"]}')
    gerenciador.concluir(tarefa)
    print(f'Depois: {type(tarefa).__name__} | concluída: {tarefa.para_dict()["concluida"]}')

print('\n========== 5. GERANDO A PRÓXIMA TAREFA RECORRENTE ==========')
proxima = recorrente.gerar_proxima(4)
print('Tarefa recorrente original:')
pprint(recorrente.para_dict())
print('Nova ocorrência gerada:')
pprint(proxima.para_dict())

print('\n========== 6. FILTRANDO POR PRIORIDADE (DEPENDÊNCIA) ==========')
print('Filtro aplicado: Prioridade.ALTA')
for tarefa in gerenciador.filtrar(Prioridade.ALTA):
    print('Resultado:', tarefa.para_dict()['titulo'])

print('\n========== 7. EDITANDO E EXCLUINDO TAREFAS ==========')
print('Antes da edição:', simples.para_dict()['titulo'])
gerenciador.editar(simples, 'Ler dois capítulos', 'Ler mais conteúdo', data_futura)
print('Depois da edição:', simples.para_dict()['titulo'])
print('Tarefas antes da exclusão:', [t.para_dict()['titulo'] for t in lista.tarefas])
gerenciador.excluir(simples)
print('Tarefas após a exclusão:', [t.para_dict()['titulo'] for t in lista.tarefas])

print('\n========== FIM DA DEMONSTRAÇÃO ==========')
