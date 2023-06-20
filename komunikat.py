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


with open('HG overall.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    current_division=""
    miejsce=1
    for row in spamreader:
        division = row[1]
        if current_division!=division:
            current_division=division
            miejsce=1
            print(f"Division:{division}")
        nazwisko,imie = row[3].split(",")
        nazwisko=nazwisko.strip()
        imie=imie.strip()

        zawodnik = get_zawodnika(imie,nazwisko)
        klub = "-----"
        if zawodnik is not None:
            klub = zawodnik.klub

        procent = row[4]
        punkty = row[5]
        region = row[9]
        print(f"{miejsce}, {nazwisko} {imie}, {klub}, {region} {procent} {punkty}")
        miejsce +=1