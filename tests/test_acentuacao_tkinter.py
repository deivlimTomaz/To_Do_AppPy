import tkinter as tk

janela = tk.Tk()
janela.title("Teste de acentuação")
janela.geometry("450x200")

tk.Label(
    janela,
    text="Digite: Cálculo, Descrição, Ação"
).pack(pady=15)

campo = tk.Entry(janela, width=40)
campo.pack(pady=10)
campo.focus_set()

janela.mainloop()
