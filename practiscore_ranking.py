import practiscore_site


class Shooter:

    def __init__(self, ps_data, ilewynikow=None):
        self.imie = ps_data['sh_fn']
        self.nazwisko = ps_data['sh_ln']
        self.klasa = ps_data['sh_dvp']
        self.ps_uuids = [ps_data['sh_uuid'],]
        self.ps_data = ps_data
        self.match_scores = {}
        try:
            self.ilewynikow = int(ilewynikow)
        except:
            self.ilewynikow = None

    def add_uuid(self, uuid):
        if uuid not in self.ps_uuids:
            self.ps_uuids.append(uuid)

    def add_match_score(self, match_id, perc):
        if match_id in self.match_scores.keys():
            raise Exception("Zawodnik ma już score w tym maczu")
        self.match_scores[match_id] = float(perc)

    def get_match_scores(self):
        if self.ilewynikow:
            return sorted(self.match_scores.values(), reverse=True)[:self.ilewynikow]
        else:
            return self.match_scores.values()

    def sum_match_scores_float(self):
        return sum(self.get_match_scores())

    def sum_match_scores(self):
        return f"{self.sum_match_scores_float():.2f}"

    def list_match_scores(self):
        return " / ".join([f"{d:.2f}" for d in self.match_scores.values()])

def find_shooter_in_db(imie, nazwisko, klasa, shooters_db ):
    for shooter in shooters_db:
        if imie==shooter.imie and nazwisko==shooter.nazwisko and klasa==shooter.klasa:
            return shooter
    return None

def find_shooter_in_db_by_uuid_klasa(uuid, klasa, shooters_db):
    for shooter in shooters_db:
        if uuid in shooter.ps_uuids and klasa==shooter.klasa:
            return shooter
    return None

def find_shooter_in_db_by_uuid(uuid, shooters_db):
    for shooter in shooters_db:
        if uuid in shooter.ps_uuids:
            return shooter
    return None

def get_ranking_from_uuids(matches_uuid, ilewynikow=None):
    shooters_db = []
    matches = []
    for match_uuid in matches_uuid:
        mdef, mresults, mscores = practiscore_site.get_match_data(match_uuid)
        print(f"Zawody {mdef['match_name'],mdef['match_date']}")
        matches.append({'nazwa':mdef['match_name'],'data':mdef['match_date']})

        # ładujemy tabelę z zawodnikami, zawodnik to imie+nazwisko+klasa w której startował
        for shooter in mdef['match_shooters']:
            sh=find_shooter_in_db(shooter['sh_fn'], shooter['sh_ln'], shooter['sh_dvp'], shooters_db)
            if sh is not None:
                sh.add_uuid(shooter['sh_uuid'])
            else:
                sh = Shooter(shooter, ilewynikow=ilewynikow)
                shooters_db.append(sh)

        print("załadowano zawodników")


        for div_data_tmp in mresults[0]['Match'][1:]:
            for div_name in div_data_tmp.keys():
                div_data = div_data_tmp[div_name]
                # print(f"Div name: {div_name}")
                for shooter_place in div_data:
                    shooter = find_shooter_in_db_by_uuid(shooter_place['shooter'], shooters_db)
                    # print(f"{shooter_place['pscPlace']} - {shooter.imie} {shooter.nazwisko}: {shooter_place['matchPercent']}")
                    shooter.add_match_score(match_uuid,shooter_place['matchPercent'])

    mdivs = {}
    for shooter in shooters_db:
        if shooter.klasa not in mdivs.keys():
            mdivs[shooter.klasa] = []
        mdivs[shooter.klasa].append(shooter)

    for klasa in mdivs.keys():
        # print(f"Wyniki dla klasy {klasa}")
        sorted_shooters = sorted(mdivs[klasa], key=lambda x: x.sum_match_scores_float(), reverse=True)
        mdivs[klasa] = sorted_shooters

        for shooter in sorted_shooters:
            print(f"{shooter.imie} {shooter.nazwisko} (punkty za edycje: {shooter.list_match_scores()}) - SUMA: {shooter.sum_match_scores()}")

    return matches, mdivs



if __name__=="__main__":

    uuids = (
        '221b2645-cb99-477a-b45e-4fd2a20ee98b', # 'ArdeaCup/Zawody_IPSC_LEV_I_pistolet_PCC_edycja_1_z_4_PLSD_Export.psc',
        'ca3f17ab-b4b0-4dcf-828f-5af689e93ad0', # 'ArdeaCup/Zawody_IPSC_LEV_I_pistolet_PCC_edycja_2_z_4_PLSD_Export.psc',
        '1241a02d-dc52-435a-9b33-c0775fd736dd', # 'ArdeaCup/Zawody_IPSC_LEV_I_pistolet_PCC_edycja_3_z_4_PLSD_Export.psc',
        'c303d286-2339-43b4-91de-b6ac297126cb', # 'ArdeaCup/Zawody_IPSC_LEV_I_pistolet_PCC_edycja_4_z_4_PLSD_Export.psc',
    )

    get_ranking_from_uuids(uuids)
