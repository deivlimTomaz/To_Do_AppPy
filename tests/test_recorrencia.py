from package.recorrencia import Recorrencia

if __name__ == "__main__":

    r = Recorrencia("semanal", 2)
    print(r)
    print(r.proxima_data())

    try:
        Recorrencia("quinzenal", 1)
    except ValueError as e:
        print("OK:", e)

    try:
        Recorrencia("diaria", True)
    except TypeError as e:
        print("OK:", e)
