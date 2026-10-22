import datetime as dt
from package.lembrete import Lembrete

if __name__ == "__main__":

    natal = Lembrete(dt.datetime(2026, 12, 25, 20, 0), "Comer rabanada")

    print(natal)
