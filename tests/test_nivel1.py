from datetime import date, timedelta

from package.categoria import Categoria
from package.gerenciador_tarefa import GerenciadorTarefa
from package.item_checklist import ItemChecklist
from package.lista import Lista
from package.prioridade import Prioridade
from package.recorrencia import Recorrencia
from package.tarefa import Tarefa
from package.tarefa_checklist import TarefaChecklist
from package.tarefa_recorr import TarefaRecorr
from package.tarefa_simples import TarefaSimples


def secao(titulo):
    print(f"\n{'=' * 65}\n{titulo}\n{'=' * 65}")


def verificar(condicao, descricao):
    assert condicao, f"FALHOU: {descricao}"
    print(f"OK - {descricao}")


def main():
    data_futura = date.today() + timedelta(days=7)

    secao('1. ASSOCIAÇÃO: CATEGORIA, LISTA E GERENCIADOR')
    categoria = Categoria('azul', 'Acadêmica')
    lista = Lista('Faculdade', categoria)
    outra_lista = Lista('Estudos extras', categoria)
    gerenciador = GerenciadorTarefa(lista)
    verificar(lista.categoria is categoria, 'Lista referencia a categoria original')
    verificar(outra_lista.categoria is categoria, 'Duas listas compartilham a categoria')
    verificar(lista.nome == 'Faculdade', 'Propriedade nome está acessível')
    print('Categoria:', lista.categoria.tipo, '-', lista.categoria.cor)

    secao('2. HERANÇA: TRÊS TIPOS DE TAREFA')
    simples = TarefaSimples(1, 'Ler capítulo', 'Leitura', Prioridade.BAIXA, data_futura)
    checklist = TarefaChecklist(2, 'Revisar POO', 'Checklist de estudos', Prioridade.ALTA, data_futura)
    recorrente = TarefaRecorr(
        3, 'Praticar Python', 'Rotina de estudo', Prioridade.MEDIA,
        date.today(), Recorrencia('semanal', 1)
    )
    for tarefa in (simples, checklist, recorrente):
        verificar(isinstance(tarefa, Tarefa), f'{type(tarefa).__name__} herda de Tarefa')
        gerenciador.criar(tarefa)
    verificar(len(lista.tarefas) == 3, 'Gerenciador cadastrou os três tipos')

    secao('3. COMPOSIÇÃO: CHECKLIST E SEUS ITENS')
    checklist.adicionar_item('Estudar herança')
    checklist.adicionar_item('Estudar polimorfismo')
    verificar(len(checklist._itens) == 2, 'Checklist possui dois itens')
    verificar(all(isinstance(item, ItemChecklist) for item in checklist._itens),
              'Itens são objetos ItemChecklist')
    try:
        gerenciador.concluir(checklist)
    except ValueError:
        print('OK - Conclusão bloqueada enquanto há itens pendentes')
    else:
        raise AssertionError('Checklist permitiu conclusão antes de marcar todos os itens')

    checklist.marcar_item(0)
    checklist.marcar_item(1)
    verificar(checklist.todos_feitos(), 'Todos os itens foram marcados')

    secao('4. POLIMORFISMO: CONCLUIR TIPOS DIFERENTES')
    for tarefa in (simples, checklist, recorrente):
        gerenciador.concluir(tarefa)
        verificar(tarefa.para_dict()['concluida'], f'{type(tarefa).__name__} foi concluída')

    secao('5. RECORRÊNCIA: DELEGAÇÃO E INDEPENDÊNCIA')
    proxima = recorrente.gerar_proxima(4)
    verificar(isinstance(proxima, TarefaRecorr), 'Nova ocorrência é TarefaRecorr')
    verificar(proxima.data_vencimento >= date.today(), 'Novo vencimento não está no passado')
    verificar(proxima._recorrencia is not recorrente._recorrencia,
              'Cada tarefa possui seu próprio objeto Recorrencia')
    verificar(proxima._recorrencia.frequencia == recorrente._recorrencia.frequencia,
              'Frequência foi preservada')
    verificar(proxima._recorrencia.intervalo == recorrente._recorrencia.intervalo,
              'Intervalo foi preservado')
    verificar(not proxima.para_dict()['concluida'], 'Nova ocorrência começa não concluída')

    secao('6. DEPENDÊNCIA: FILTRAGEM COM PRIORIDADE')
    filtradas = gerenciador.filtrar(Prioridade.ALTA)
    verificar(len(filtradas) == 1 and filtradas[0] is checklist,
              'Gerenciador utiliza Prioridade para filtrar tarefas')

    secao('7. OPERAÇÕES DO GERENCIADOR')
    gerenciador.editar(simples, 'Ler dois capítulos', 'Leitura ampliada', data_futura)
    verificar(simples.para_dict()['titulo'] == 'Ler dois capítulos', 'Edição alterou o título')
    gerenciador.excluir(simples)
    verificar(len(lista.tarefas) == 2, 'Exclusão removeu a tarefa da lista')
    try:
        gerenciador.criar(TarefaSimples(
            99, 'Tarefa vencida', 'Não pode ser cadastrada',
            Prioridade.BAIXA, date.today() - timedelta(days=1)
        ))
    except ValueError:
        print('OK - Cadastro de tarefa vencida bloqueado')
    else:
        raise AssertionError('Cadastro aceitou uma tarefa com data passada')

    secao('RESULTADO FINAL')
    print('SUCESSO: demonstração integrada do Nível 1 concluída!')
    print('Conceitos demonstrados: herança, polimorfismo, composição, associação e dependência.')


if __name__ == '__main__':
    main()
