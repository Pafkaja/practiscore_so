import csv
from region import get_zawodnikow_ze_strony_regionu

zawodnicy_regionu = get_zawodnikow_ze_strony_regionu()

def zamien_pl_znaki(input):
    zpl = "ąęśćźżłóń"
    zen = "aesczzlon"

    output = input.lower()
    for i in range(len(zpl)):
        output = output.replace(zpl[i],zen[i])

    return output

def get_zawodnika(imie, nazwisko):
    for zaw in zawodnicy_regionu:
        if zamien_pl_znaki(zaw.imie) == zamien_pl_znaki(imie) and zamien_pl_znaki(zaw.nazwisko) == zamien_pl_znaki(nazwisko):
            return zaw


with open('PCC overall.csv', 'r') as f:

    lines = f.readlines()

with open('PCC overall_klubs.csv', 'w') as f:

    for row in lines:
        sline = row.split('\t')
        if len(sline)<5:
            f.write(row)
            continue

        if sline[0]=='Msc':
            f.write(row)
            continue

        zawodnik = get_zawodnika(sline[5],sline[4])
        klub = "-----"
        if zawodnik is not None:
            klub = zawodnik.klub

        sline = [s.strip() for s in sline if s !='\n']
        sline.append(klub)
        sline.append('\n')
        f.write('\t'.join(sline))
