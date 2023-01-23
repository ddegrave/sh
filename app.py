from flask import Flask, render_template, request, jsonify, flash
from pythermalcomfort.models import pmv_ppd

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/', methods=['GET', 'POST'])
def index():
    tdb = float(request.form['tdb'])
    tr = float(request.form['tr'])
    vr = float(request.form['vr'])
    rh = float(request.form['rh'])
    met = float(request.form['met'])
    clo = float(request.form['clo'])
    wme = 0
    pmv_value=pmv_ppd(tdb, tr, vr, rh, met, clo,wme)
    return render_template('index.html', pmv_value=pmv_value, tdb=tdb, tr=tr, vr=vr, rh=rh, met=met,clo=clo)


if __name__ == '__main__':
    app.run(debug=True)