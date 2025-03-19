import matplotlib.pyplot as plt
from openpyxl import Workbook
import re

file=open("../data/time.txt")
file2=open("../data/intensity.txt")
intense=[]
time=[]
for i in file:
    line=i.strip()
    line=int(line)
    time.append(line)
suma=sum(time)
avgTime=suma/len(time)
print(avgTime)

for k in file2:
    lineIntensity = k.split()
    lineIntensity[1]=float(lineIntensity[1])
    #lineIntensity=[float(match) for match in re.findall(r"[-+]?\d*\.\d+E[-+]?\d+", lineIntensity)]
    intense.append(lineIntensity)



'''def zapisz_do_excela(wyniki, plik_excel, nazwa_arkusza="Arkusz1"):
    """
    Zapisuje wyniki do pliku Excel w kolejnych wierszach.

    :param wyniki: Lista wyników (każdy element listy może być listą lub krotką reprezentującą jeden wiersz).
    :param plik_excel: Nazwa pliku Excel, do którego zapisać dane.
    :param nazwa_arkusza: Nazwa arkusza w pliku Excel.
    """
    # Utwórz nowy plik Excel
    workbook = Workbook()
    arkusz = workbook.active
    arkusz.title = nazwa_arkusza

    # Iteracja przez wyniki i zapis do kolejnych wierszy
    for idx, wiersz in enumerate(wyniki, start=1):
        for kolumna_idx, wartosc in enumerate(wiersz, start=1):
            arkusz.cell(row=idx, column=kolumna_idx, value=wartosc)

    # Zapisz plik
    workbook.save(plik_excel)
    print(f"Wyniki zapisano w pliku {plik_excel}")

'''
#zapisz_do_excela(intense, "wyniki.xlsx")
print(intense)
