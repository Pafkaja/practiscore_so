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
    fname = "Pomorze_Open_2023_HG_PCC_L3_Export.psc"

    match_data = get_match_data(fname)


    # match_score = get_match_scores(fname)
    #
    # tmp_score = match_score['match_scores'][0]['stage_stagescores'][0]['ts']
    #
    # for score in tmp_score:
    #     idx=0
    #     labels = ("A","B","C","D","NS","M","NPM")
    #     print("---")
    #     while score>0:
    #         print(f"{labels[idx]}: {score&0xF}")
    #         score = score >> 4
    #         idx +=1

    #clone match data to two separate ones
    match_data_hg = json.loads(json.dumps(match_data))
    match_data_pcc = json.loads(json.dumps(match_data))

    # match_data_hg['match_id'] = str(uuid.uuid4())
    # match_data_pcc['match_id'] = str(uuid.uuid4())
    match_data_hg['match_id'] = "83f62524-1e99-4cb7-a174-c00a9e39a783"
    match_data_pcc['match_id'] = "2e20f76a-6d44-41dd-afab-7b07a6e3d189"

    match_data_hg['match_name'] = "Pomorze Open 2023 HG"
    match_data_pcc['match_name'] = "Pomorze Open 2023 PCC"

    match_shooters_hg = []
    match_shooters_pcc = []
    for shooter in match_data['match_shooters']:
        shooter['sh_ln'] = shooter['sh_ln'].upper()
        shooter['sh_fn'] = shooter['sh_fn'].title()
        if shooter['sh_dvp'].startswith("PCC"):
            match_shooters_pcc.append(shooter)
        else:
            match_shooters_hg.append(shooter)
    match_data_hg['match_shooters']=match_shooters_hg
    match_data_pcc['match_shooters'] = match_shooters_pcc


    match_stages_hg = []
    match_stages_pcc = []
    for stage in match_data['match_stages']:
        if "PCC" in stage['stage_name']:
            match_stages_pcc.append(stage)
        else:
            match_stages_hg.append(stage)
    match_data_hg['match_stages'] = match_stages_hg
    match_data_pcc['match_stages'] = match_stages_pcc

    with open("HG/match_def.json","w") as f:
        json.dump(match_data_hg,f, indent=4)
    with open("PCC/match_def.json","w") as f:
        json.dump(match_data_pcc,f, indent=4)



