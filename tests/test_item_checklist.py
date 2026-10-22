from package.item_checklist import ItemChecklist

if __name__ == "__main__":
    
    tarefa = ItemChecklist("Acordar 7h")
    print(tarefa)

    tarefa.marcar()

    print(tarefa)

    print(tarefa.feito)
