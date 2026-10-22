import datetime as dt
from package.prioridade import Prioridade
from package.lembrete import Lembrete

def main():
    
    print(list(Prioridade))

    natal = Lembrete(dt.datetime(2026, 12, 25, 20, 0), "Comer rabanada")
    
    print(natal)

    print("\n--- TESTANDO A PROTEÇÃO DE APENAS LEITURA ---")
    try:
        # Tentando alterar a mensagem diretamente (o Python deve impedir)
        natal.mensagem = "Mudar o texto"
    except AttributeError as e:
        print(f"Sucesso! O Python bloqueou a alteração direta. Erro: {e}")

if __name__ == "__main__":
    main()
