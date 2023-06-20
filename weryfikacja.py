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

def get_shooter(match_data, shooter_id):
    for shooter in match_data['match_shooters']:
        if shooter['sh_uid']==shooter_id:
            return shooter

def get_stage(match_data, stage_number):
    for stage in match_data['match_stages']:
        if str(stage['stage_number'])==stage_number:
            return stage['stage_name']


class Score:
    def __init__(self, score_data, match_data):
        self.labels = ("A", "B", "C", "D", "NS", "M", "NPM", "Proc", "time", "pts")
        for l in self.labels:
            setattr(self,l,0)

        self.match_data = match_data

        if 'dqs' in score_data.keys():
            self.DQ=True
            self.dq_reason = self.fill_dq(score_data['dqs'])
            return
        else:
            self.DQ=False

        if 'dnf' in score_data.keys():
            return

        for score in score_data['ts']:
            idx=0
            while score>0:
                cur_nr = getattr(self,self.labels[idx])
                scr = score & 0xF
                setattr(self, self.labels[idx], cur_nr+scr)
                score = score >> 4
                idx +=1

        self.A += score_data['poph']
        self.M += score_data['popm']
        if "proc" in score_data.keys():
            self.Proc = score_data['proc']

        self.time = score_data['str'][0]
        self.pts = score_data['rawpts']

    def find_dq(self,uuid):
        for dq_uuid in self.match_data['match_dqs']:
            if dq_uuid['uuid']==uuid:
                return dq_uuid

    def fill_dq(self, dq_uuids):
        result=""
        for uuid in dq_uuids:
            dq = self.find_dq(uuid)
            if dq:
                result = f"{result} {dq['name']}"
        return result.strip()


    def __str__(self):
        result = ""
        for l in self.labels:
            result = f"{result} {getattr(self,l)} "
        return result

if __name__=="__main__":
    fname = "Pomorze_Open_2023_HG_ExportFinal.psc"

    match_data = get_match_data(fname)
    match_score = get_match_scores(fname)

    match_scores = match_score['match_scores']

    for stage in match_scores:
        stage_nr = get_stage(match_data,stage['stage_number'])
        print('<table class="po-table table table-striped table-sm table-hover">')
        print(f"<tr><th>STAGE: {stage_nr}<th>Time</th><th>Points</th><th>A</th><th>C</th><th>D</th><th>M</th><th>NS</th><th>Proc</th></tr>")
        for stage_score in stage['stage_stagescores']:
            shooter_id = stage_score['shtr']
            shooter = get_shooter(match_data, shooter_id)
            scr = Score(stage_score, match_data)

            line = f"<tr><td>{shooter['sh_ln'].upper()} {shooter['sh_fn'].title()}</td>"
            if scr.DQ:
                line = f'{line}<td colspan="8">DQ {scr.dq_reason}</td></tr>'
            else:
                line = f"{line}<td>{scr.time}</td><td>{scr.pts}</td><td>{scr.A}</td><td>{scr.C}</td><td>{scr.D}</td><td>{scr.M}</td><td>{scr.NS}</td><td>{scr.Proc}</td></tr>"
            print(line)
        print(f"</table>")


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

    print()



