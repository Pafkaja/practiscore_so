import zipfile
import json
import uuid

def get_match_data(fname):
    with zipfile.ZipFile(fname) as psczip:
        with psczip.open('match_def.json') as match_def_file:
            return json.load(match_def_file)


def get_match_scores(fname):
    with zipfile.ZipFile(fname) as psczip:
        with psczip.open('match_scores.json') as match_scores_file:
            return json.load(match_scores_file)

if __name__=="__main__":
    fname = "Pomorze_Open_2023_HG_Export.psc"

    match_data = get_match_data(fname)

    divisions = {}

    for shooter in match_data['match_shooters']:
        if shooter["sh_dvp"] not in divisions.keys():
            divisions[shooter["sh_dvp"]] = {}

        if "sh_ctgs" not in shooter.keys():
            shooter["sh_ctgs"] = '["Regular"]'

        for ctg in json.loads(shooter["sh_ctgs"]):
            if ctg not in divisions[shooter["sh_dvp"]].keys():
                divisions[shooter["sh_dvp"]][ctg] = []
        divisions[shooter["sh_dvp"]][ctg].append(shooter)


    for div in divisions.keys():
        total = 0
        classes = []
        for cls in divisions[div].keys():
            if len(divisions[div][cls])>=5:
                classes.append(cls)
            total += len(divisions[div][cls])

        if total>=10:
            print(f"{div}")
            for cls in classes:
                if cls=="Regular":
                    continue
                print(f"{div} {cls}")


    print()