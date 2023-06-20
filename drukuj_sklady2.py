import zipfile
import json
import uuid

def get_match_data(fname):
    with zipfile.ZipFile(fname) as psczip:
        with psczip.open('match_def.json') as match_def_file:
            return json.load(match_def_file)

if __name__=="__main__":
    fname = "Pomorze_Open_2023_PCC_Export.psc"

    match_data = get_match_data(fname)

    squads = {}
    for shooter in match_data['match_shooters']:
        if shooter["sh_sqd"] not in squads.keys():
            squads[shooter["sh_sqd"]] = []
        squads[shooter["sh_sqd"]].append(shooter)

    for sname in sorted(squads.keys()):
        print('<table class="po-table table table-borderless table-striped table-sm table-hover">'
              '		<thead> '
              f'<tr><th>Skład {sname}</th></tr>'
              '</thead><tbody>')
        sorted_by_name = sorted(squads[sname], key=lambda x: x['sh_ln'].upper())
        for shooter in sorted_by_name:
            print(f"<tr><td>{shooter['sh_ln'].upper()} {shooter['sh_fn'].title()}</td>")

            if "sh_ctgs" not in shooter.keys():
                shooter["sh_ctgs"] = '["Regular"]'
            klases = ""
            for ctg in json.loads(shooter["sh_ctgs"]):
                if ctg not in ["Regular"]:
                    klases = f"{klases} {ctg}"


            print(f"<td>{shooter['sh_dvp']}</td><td>{shooter['sh_pf']}</td><td>{klases}</td></tr>")

        print('</tbody> </table>')





