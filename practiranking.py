from flask import Flask, request, render_template, make_response
from urllib.parse import urlparse
import re
import practiscore_ranking
import io
import csv

app = Flask(__name__, template_folder='templates')

'''
https://practiscore.com/results/new/c303d286-2339-43b4-91de-b6ac297126cb
https://practiscore.com/results/new/1241a02d-dc52-435a-9b33-c0775fd736dd
https://practiscore.com/results/new/ca3f17ab-b4b0-4dcf-828f-5af689e93ad0
https://practiscore.com/results/new/221b2645-cb99-477a-b45e-4fd2a20ee98b
'''


@app.route('/practiscore',methods=['GET', 'POST'])
def index():
    render_data = {}
    if request.method == "POST":
        match_uuids = []
        form_urls = request.form.get("urls")
        for fu in form_urls.split():
            url_parsed = urlparse(fu)
            if url_parsed.scheme and url_parsed.netloc:
                muuid = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', url_parsed.path)
                if len(muuid)>0:
                    match_uuids.append(muuid[0])
        if len(match_uuids)>1:
            matches, results = practiscore_ranking.get_ranking_from_uuids(match_uuids)
            render_data = {'matches':matches, 'results':results, 'form_urls':form_urls}
            if request.form.get("action")=="Generuj csv":
                si = io.StringIO()
                cw = csv.writer(si)

                for m in matches:
                    cw.writerow([])
                    cw.writerow([m['data'],m['nazwa']])

                for div in results.keys():
                    cw.writerow([])
                    cw.writerow([div,])
                    cw.writerow(['Nazwisko','Imie','punkty poszczegolnych edycji','SUMA' ])
                    for shooter in results[div]:
                        cw.writerow([shooter.nazwisko, shooter.imie, shooter.list_match_scores(), shooter.sum_match_scores()])
                output = make_response(si.getvalue())
                output.headers["Content-Disposition"] = "attachment; filename=export.csv"
                output.headers["Content-type"] = "text/csv"
                return output
    return render_template('index.html', data=render_data)
