import pandas
import json

'''practi: importuj eksportuj, eksportuj zawody, zapisz na karcie SD, na dysk google, unzipuj i podmień match_def.json'''


class Zawodnik:
    def __init__(self, imie, nazwisko, klub, nr_licencji, alias):
        self.imie = imie
        self.nazwisko = nazwisko
        self.klub = klub
        self.nr_licencji = nr_licencji
        self.alias = alias

    def __repr__(self):
        return "%s %s (%s), %s, %s" % (self.imie, self.nazwisko, self.alias, self.klub, self.nr_licencji)

def get_zawodnikow_ze_strony_regionu():
    tables_on_page = pandas.read_html("https://ipsc-pl.org/region-polska/lista-zawodnikow-2023")
    table = tables_on_page[0]
    zawodnicy_json = table.to_dict(orient='list')
    zawodnicy_nazwiska = [z.lower() for z in zawodnicy_json[1]]
    zawodnicy_imiona = [z.lower() for z in zawodnicy_json[2]]

    result = []
    for i in range(len(zawodnicy_json[0])):
        try:
            nr_licenecji = int(zawodnicy_json[0][i])
            result.append( Zawodnik(zawodnicy_json[2][i],zawodnicy_json[1][i], zawodnicy_json[3][i], nr_licenecji, zawodnicy_json[4][i]))
        except ValueError:
            print("%s %s" % (zawodnicy_json[2][i],zawodnicy_json[1][i]))

    return result

if __name__=="__main__":
    zaw = get_zawodnikow_ze_strony_regionu()
    for z in sorted(zaw, key=lambda x: x.nr_licencji):
        print(z)